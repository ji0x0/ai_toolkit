import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/bootstrap.py'


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = self.enterContext(tempfile.TemporaryDirectory())
        self.root = Path(self.temp).resolve() / 'task with spaces'
        self.root.mkdir()
        (self.root / 'README.md').write_text('Actual task. Extra record files are forbidden until checked.\n')
        (self.root / 'AGENTS.md').write_text('Existing task instructions\n')
        (self.root / 'main.py').write_text('value = 1\n')

    def run_bootstrap(self, *args, env=None, cwd=ROOT, check=True):
        result = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, env=env,
                                capture_output=True, text=True, timeout=10)
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        return result

    def test_handoff_installs_skills_preserves_task_and_returns_readable_entry(self):
        before = {name: (self.root / name).read_bytes() for name in ['README.md', 'AGENTS.md', 'main.py']}
        result = self.run_bootstrap('--target', str(self.root))
        self.assertEqual(result['status'], 'ready')
        self.assertTrue(result['continue_in_current_session'])
        self.assertEqual(result['target'], str(self.root))
        self.assertEqual(result['entry_skill'], 'solve-task')
        self.assertEqual(Path(result['entry_path']), self.root / '.agents/skills/solve-task/SKILL.md')
        self.assertTrue(Path(result['entry_path']).is_file())
        self.assertEqual(len(result['skills']), 7)
        for skill in result['skills']:
            self.assertTrue(skill['description'])
            self.assertTrue(Path(skill['path']).is_file())
            self.assertEqual(skill['action'], 'install')
        self.assertEqual(set(result['task_instruction_paths']), {str(self.root / name) for name in ['README.md', 'AGENTS.md']})
        for name, content in before.items():
            self.assertEqual((self.root / name).read_bytes(), content)
        for name in ['devlog.md', 'probe.md', '.local', 'frontend', 'backend']:
            self.assertFalse((self.root / name).exists(), name)

    def test_repeat_is_idempotent_and_preserves_existing_task_records(self):
        self.run_bootstrap('--target', str(self.root))
        (self.root / 'probe.md').write_text('Actual decisions\n')
        (self.root / 'devlog.md').write_text('Actual task history\n')
        result = self.run_bootstrap('--target', str(self.root))
        self.assertTrue(all(s['action'] == 'unchanged' for s in result['skills']))
        self.assertEqual((self.root / 'probe.md').read_text(), 'Actual decisions\n')
        self.assertEqual((self.root / 'devlog.md').read_text(), 'Actual task history\n')

    def test_explicit_target_is_required_and_distribution_is_refused(self):
        self.assertNotEqual(self.run_bootstrap(cwd=self.root, check=False).returncode, 0)
        self.assertFalse((self.root / '.agents').exists())
        result = self.run_bootstrap('--target', str(ROOT), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((ROOT / 'devlog.md').exists())
        self.assertFalse((ROOT / 'probe.md').exists())

    def test_existing_different_skill_blocks_other_installs(self):
        path = self.root / '.agents/skills/solve-task/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('Existing different user skill\n')
        result = self.run_bootstrap('--target', str(self.root), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(path.read_text(), 'Existing different user skill\n')
        self.assertEqual([p.name for p in path.parent.parent.iterdir()], ['solve-task'])

    def test_bootstrap_does_not_spawn_codex_or_start_watcher(self):
        binary = Path(self.temp).resolve() / 'bin'
        binary.mkdir()
        sentinel = self.root / 'nested-codex.txt'
        fake = binary / 'codex'
        fake.write_text('#!' + sys.executable + '\nfrom pathlib import Path\nPath(' + repr(str(sentinel)) + ').write_text("started")\n')
        fake.chmod(0o700)
        env = dict(os.environ, PATH=str(binary) + os.pathsep + os.environ.get('PATH', ''))
        self.run_bootstrap('--target', str(self.root), env=env)
        self.assertFalse(sentinel.exists())
        self.assertFalse((self.root / '.local').exists())
        self.assertFalse((self.root / '.git').exists())


if __name__ == '__main__':
    unittest.main()
