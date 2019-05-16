#!/usr/bin/env python3

import subprocess
import typing as t
import unittest
from unittest.mock import patch

from src.cli_wrappers.generic_cli_wrapper import (
    CliCommandFailed,
    GenericCliWrapper,
)

class TestGenericCliWrapper(unittest.TestCase):
    """
    The unit tests for the GenericCliWrapper class.
    """
    @staticmethod
    def _make_dummy_cli_wrapper() -> GenericCliWrapper:
        class _DymmyCliWrapper(GenericCliWrapper):
            _CLI_BINARY: t.ClassVar[str] = "dummy_cli"
            _VERSION_ARGUMENT = '--version'
            _SHELL_REQUIRED = True

        return _DymmyCliWrapper
    

    @patch.object(
        GenericCliWrapper,
        "_run_cli"
    )
    def test_get_version(
        self,
        mock_run_cli
    ) -> None:
        """
        Verify that GenericCliWrapper.get_version() works correctly.
        """
        mock_run_cli.return_value="dummy version"
        self.assertEqual(self._make_dummy_cli_wrapper().get_version(),"dummy version")
        mock_run_cli.assert_called_with(['--version'],log_output=False)
    
    
    @patch.object(
        subprocess,
        "run"
    )
    def test_cli_failure(
        self,
        mock_run
    ) -> None:
        """
        Verify that cli cient fails with proper message
        """
        mock_run.return_value = subprocess.CompletedProcess(
            args="fake_arguments",
            returncode = 125,
            stdout=b'',
            stderr=b'Command not found'
        )
        with self.assertRaises(CliCommandFailed) as context:
            self._make_dummy_cli_wrapper()._run_cli(["abc","xyz"])

        self.assertEqual(
            "Unable to execute dummy_cli CLI, error=125",
            str(context.exception),
        )
        mock_run.assert_called_once_with(
            ['dummy_cli','abc','xyz'],
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )


    @patch.object(
    subprocess,
    "run"
    )
    def test_cli_success(
        self,
        mock_run
    ) -> None:
        """
        Verify that cli cient success with proper results
        """
        mock_run.return_value = subprocess.CompletedProcess(
            args="fake_arguments",
            returncode = 0,
            stdout=b'fake results',
            stderr=b''
        )
        self.assertEqual(
            "fake results",
            self._make_dummy_cli_wrapper()._run_cli(["fake_arguments"]),
        )
        mock_run.assert_called_once_with(
            ['dummy_cli','fake_arguments'],
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )
