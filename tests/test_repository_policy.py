"""Public STROJ GitOps repository contract. This does not test V7 runtime code."""
import pathlib
import re
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOWLIST = {
    '.gitignore', 'README.md', 'CONTRIBUTING.md',
    '.github/workflows/quality.yml', '.github/pull_request_template.md',
    'docs/STROJ_V7_WORKFLOW.md', 'tests/test_repository_policy.py',
    'datadog/README.md', 'datadog/compose.yaml', 'datadog/.env.example',
}


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def tracked():
    return {p for p in git('ls-files', '-z').split('\x00') if p}


class PublicRepoContract(unittest.TestCase):
    def test_only_reviewed_allowlisted_paths(self):
        self.assertEqual(tracked(), ALLOWLIST,
                         'Public repo contains unreviewed files or required files are missing')

    def test_credentials_and_live_state_not_tracked(self):
        bad_suffixes = ('.key', '.pem', '.db', '.db-wal', '.sqlite', '.sqlite3',
                        '.zfo', '.eml', '.jsonl', '.log', '.zip', '.tar', '.bak')
        for rel in tracked():
            name = pathlib.PurePosixPath(rel).name.lower()
            self.assertFalse(rel.startswith(('runtime/', 'ha-config/', 'backups/', 'secrets/')),
                             rel)
            self.assertFalse(name.endswith(bad_suffixes), rel)
            self.assertFalse(('.env' in name and name != '.env.example'), rel)
            self.assertNotIn('token', name, rel)
            self.assertNotIn('secret', name, rel)
            self.assertNotIn('private', name, rel)

    def test_known_credential_shapes_are_absent(self):
        # Concatenate marker parts to avoid matching this test's own source.
        private_key = b'-----BEGIN ' + b'PRIVATE KEY-----'
        ssh_private = b'-----BEGIN OPENSSH ' + b'PRIVATE KEY-----'
        jwt_like = re.compile(rb'eyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{12,}')
        gh_token = re.compile(rb'gh' + rb'[pousr]_[A-Za-z0-9]{30,}')
        for rel in tracked():
            body = (ROOT / rel).read_bytes()
            self.assertLess(len(body), 2_000_000, 'Unexpected binary/large file: '+rel)
            self.assertNotIn(private_key, body, rel)
            self.assertNotIn(ssh_private, body, rel)
            self.assertIsNone(jwt_like.search(body), rel)
            self.assertIsNone(gh_token.search(body), rel)

    def test_sensitive_names_ignored(self):
        for rel in ('datadog/.env', 'secrets/api-token.txt',
                    'backups/ha.tar', 'runtime/home-assistant_v2.db',
                    'runtime/events.jsonl', 'private.key'):
            check = subprocess.run(['git', 'check-ignore', '--no-index', '-q', rel],
                                   cwd=ROOT)
            self.assertEqual(check.returncode, 0, 'Sensitive file not ignored: '+rel)
        for rel in ('.github/workflows/quality.yml', 'tests/test_repository_policy.py'):
            check = subprocess.run(['git', 'check-ignore', '--no-index', '-q', rel],
                                   cwd=ROOT)
            self.assertEqual(check.returncode, 1, 'Quality source ignored: '+rel)

    def test_workflow_has_no_deploy_and_minimal_permissions(self):
        body = (ROOT / '.github/workflows/quality.yml').read_text()
        self.assertIn('permissions:\n  contents: read', body)
        self.assertIn('persist-credentials: false', body)
        self.assertIn('python -m unittest discover -s tests -v', body)
        self.assertNotIn('pull_request_target:', body)
        self.assertNotIn('workflow_run:', body)
        self.assertNotIn('secrets.', body)
        self.assertNotIn('docker compose up', body)
        self.assertNotIn('ssh ', body)

    def test_datadog_requires_explicit_opt_in(self):
        template = (ROOT / 'datadog/compose.yaml').read_text()
        example = (ROOT / 'datadog/.env.example').read_text()
        self.assertIn('DD_API_KEY: ${DD_API_KEY:?', template)
        self.assertIn("DD_LOGS_ENABLED: 'false'", template)
        self.assertIn("DD_APM_ENABLED: 'false'", template)
        self.assertRegex(example, r'(?m)^DD_API_KEY=\s*$')


if __name__ == '__main__':
    unittest.main()
