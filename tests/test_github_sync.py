import unittest

from scripts.github_sync import validate_repo_path


class TestGitHubSyncPathSafety(unittest.TestCase):
    def test_accepts_repo_relative_path(self):
        self.assertEqual(validate_repo_path("scripts/utility.py"), "scripts/utility.py")

    def test_rejects_empty_path(self):
        with self.assertRaises(ValueError):
            validate_repo_path("")

    def test_rejects_absolute_path(self):
        with self.assertRaises(ValueError):
            validate_repo_path("/etc/passwd")

    def test_rejects_parent_traversal(self):
        for value in ("../secret", "scripts/../../secret", "scripts/../secret"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_repo_path(value)

    def test_rejects_dot_and_empty_segments(self):
        for value in (".", "scripts/./helper.py", "scripts//helper.py"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_repo_path(value)

    def test_rejects_backslash_and_nul(self):
        for value in ("scripts\\helper.py", "scripts/\x00helper.py"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_repo_path(value)


if __name__ == "__main__":
    unittest.main()
