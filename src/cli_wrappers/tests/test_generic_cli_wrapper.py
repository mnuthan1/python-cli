#!/usr/bin/env python3

import subprocess
import typing as t
import unittest
import unittest.mock
import genty

from src.cli_wrappers.generic_cli_wrapper import (
    CliCommandFailed,
    GenericCliWrapper,
)

@genty.genty
class TestGenericCliWrapper(unittest.TestCase):
    """
    The unit tests for the GenericCliWrapper class.
    """
    @staticmethod
    def _make_dummy_cli_wrapper(use_shell:bool) -> GenericCliWrapper:
        class _DymmyCliWrapper(GenericCliWrapper):
            _CLI_BINARY: t.ClassVar[str] = "dummy_cli"
            _VERSION_ARGUMENT = '--version'
            _SHELL_REQUIRED = use_shell

        return _DymmyCliWrapper
    """
    The unit tests for the GenericCliWrapper class with out _CLI_BINARY.
    """
    @staticmethod
    def _make_dummy_cli_wrapper_without_binary(use_shell:bool) -> GenericCliWrapper:
        class _DymmyCliWrapperWithoutBinary(GenericCliWrapper):
            _VERSION_ARGUMENT = '--version'
            _SHELL_REQUIRED = use_shell

        return _DymmyCliWrapperWithoutBinary

    
    @genty.genty_dataset(
        wiht_shell=(True,),
        without_shell=(False,),
    )
    @unittest.mock.patch.object(
        GenericCliWrapper,
        "_run_cli",
    )
    def test_get_version(
        self,
        use_shell:bool,
        mock_run_cli
    ) -> None:
        """
        Verify that GenericCliWrapper.get_version() works correctly.
        """
        mock_run_cli.return_value="dummy version"
        self.assertEqual(self._make_dummy_cli_wrapper(use_shell).get_version(),"dummy version")
        mock_run_cli.assert_called_with(['--version'],log_output=False)
    
    
    @genty.genty_dataset(
        wiht_shell=(True,),
        without_shell=(False,),
    )
    @unittest.mock.patch.object(
        subprocess,
        "run"
    )
    def test_cli_failure(
        self,
        use_shell:bool,
        mock_run
    ) -> None:
        """
        Verify that cli cient fails with proper message
        """
        #use_shell=True
        mock_run.return_value = subprocess.CompletedProcess(
            args="fake_arguments",
            returncode = 125,
            stdout=b'',
            stderr=b'Command not found'
        )
        dummy_cli = self._make_dummy_cli_wrapper(use_shell)
        dummy_cli._CWD = "/Users/Dummy/"
        with self.assertRaises(CliCommandFailed) as context:
            dummy_cli._run_cli(["abc","xyz"])

        self.assertEqual(
            "Unable to execute dummy_cli CLI, error=125",
            str(context.exception),
        )
        mock_run.assert_called_once_with(
            ['dummy_cli','abc','xyz'],
            shell=use_shell,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd="/Users/Dummy/"
        )
    @genty.genty_dataset(
        (True,True),
        (False,True),
        (False,False),
        (True,False),
    )
    @unittest.mock.patch.object(
    subprocess,
    "run"
    )
    def test_cli_success(
        self,
        use_shell:bool,
        log_output:bool,
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
            self._make_dummy_cli_wrapper(use_shell)._run_cli(["fake_arguments"],log_output=log_output),
        )
        mock_run.assert_called_once_with(
            ['dummy_cli','fake_arguments'],
            shell=use_shell,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd=None
        )
    
    @genty.genty_dataset(
        with_log=(True,),
        without_log=(False,)
    )
    @unittest.mock.patch.object(
    subprocess,
    "run"
    )
    def test_cli_suprocess_exception(
        self,
        log_output:bool,
        mock_run
    ) -> None:
        """
        Verify that cli cient success with proper results
        """
        mock_run.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):  # passes
            self._make_dummy_cli_wrapper(True)._run_cli(["fake_arguments"],log_output=log_output)
            
        mock_run.assert_called_once_with(
            ['dummy_cli','fake_arguments'],
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd=None
        )

    @genty.genty_dataset(
        wiht_shell=(True,),
        without_shell=(False,),
    )
    @unittest.mock.patch.object(
    subprocess,
    "run"
    )
    def test_cli_success_without_binary(
        self,
        use_shell:bool,
        mock_run
    ) -> None:
        """
        Verify that cli cient success with proper results
        """
        mock_run.return_value = subprocess.CompletedProcess(
            args="fake_arguments",
            returncode = 1,
            stdout=b'fake results',
            stderr=b''
        )
        self.assertRaises(
            CliCommandFailed,
            lambda:self._make_dummy_cli_wrapper_without_binary(use_shell)._run_cli(["fake_arguments"]),
        )
        mock_run.assert_not_called()
