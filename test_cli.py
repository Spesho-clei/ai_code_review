import unittest
from unittest.mock import patch, MagicMock
import cli


class TestCodeReviewAssistant(unittest.TestCase):

    @patch('subprocess.run')
    def test_run_pylint_no_issues(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        with patch('builtins.print') as mocked_print:
            cli.run_pylint("test_file.py")
            mocked_print.assert_called_with(f"\x1b[32mPylint: No issues found in test_file.py\n\x1b[0m")

    @patch('subprocess.run')
    def test_run_flake8_no_issues(self, mock_run):
        mock_run.return_value = MagicMock(stdout="")
        with patch('builtins.print') as mocked_print:
            cli.run_flake8("test_file.py")
            mocked_print.assert_called_with(f"\x1b[32mFlake8: No issues found in test_file.py\n\x1b[0m")

    @patch('subprocess.run')
    def test_run_bandit_no_issues(self, mock_run):
        mock_run.return_value = MagicMock(stdout="No issues identified")
        with patch('builtins.print') as mocked_print:
            cli.run_bandit("test_file.py")
            mocked_print.assert_called_with(f"\x1b[32mBandit: No security issues found in test_file.py\n\x1b[0m")

    @patch('subprocess.run')
    def test_run_flake8_with_issues(self, mock_run):
        mock_run.return_value = MagicMock(stdout="test_file.py:1:1: F401 Unused import sys")
        with patch('builtins.print') as mocked_print:
            cli.run_flake8("test_file.py")
            mocked_print.assert_called()
            self.assertIn("Flake8 Results:", mocked_print.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
