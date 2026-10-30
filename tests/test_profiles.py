from pathlib import Path
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('profile_installer', ROOT / 'tools/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def test_fullstack_preview_then_install_and_repeat(self):
        plan = installer.install(self.root, ['record-work'], profile='fullstack')
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertTrue(any(name == 'file:frontend/package-lock.json' for name, action in plan))
        installer.install(self.root, ['record-work'], True, profile='fullstack')
        for path in ['frontend/src/App.tsx', 'backend/app/main.py', 'ai/rag.py', 'data/train.py', 'Dockerfile', 'compose.yaml', 'devlog.md', 'probe.md']:
            self.assertTrue((self.root / path).is_file(), path)
        self.assertFalse((self.root / 'frontend/node_modules').exists())
        self.assertTrue(all(action == 'unchanged' for _, action in installer.install(self.root, ['record-work'], True, profile='fullstack')))

    def test_backend_resolves_dependencies_but_not_frontend_or_infra(self):
        installer.install(self.root, [], True, profile='api')
        for folder in ['backend', 'ai', 'data']:
            self.assertTrue((self.root / folder).is_dir())
        self.assertFalse((self.root / 'frontend').exists())
        self.assertFalse((self.root / 'Dockerfile').exists())

    def test_file_conflict_prevents_skills_records_and_other_files(self):
        (self.root / 'frontend').mkdir()
        (self.root / 'frontend/package.json').write_text('existing project')
        with self.assertRaises(ValueError):
            installer.install(self.root, ['record-work'], True, profile='fullstack')
        self.assertEqual((self.root / 'frontend/package.json').read_text(), 'existing project')
        self.assertFalse((self.root / '.agents').exists())
        self.assertFalse((self.root / 'ai').exists())
        self.assertFalse((self.root / 'devlog.md').exists())

    def test_symlink_parent_is_not_followed(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / 'frontend').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(self.root, [], True, profile='fullstack')
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_unknown_profile_or_module_rejected_without_mutation(self):
        for selection in [{'profile': 'missing'}, {'modules': ['unknown']}, {'profile': 'api', 'modules': ['ai']}]:
            with self.assertRaises(ValueError):
                installer.install(self.root, [], True, **selection)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
