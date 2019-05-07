#!/usr/bin/env python3


import subprocess
import typing as t
import pytest


from src.cli_wrappers.generic_cli_wrapper import (
    CliCommandFailed,
    GenericCliWrapper,
)

class TestGenericCliWrapper:
    """
    The unit tests for the GenericCliWrapper class.
    """

    
    def test_get_version(
        self,
    ) -> None:
        """
        Verify that GenericCliWrapper.get_version() works correctly.

        """
        GenericCliWrapper._SHELL_REQUIRED=False
        GenericCliWrapper._CLI_BINARY="/bin/bash"
        GenericCliWrapper._VERSION_ARGUMENT="--version"
        
        result = GenericCliWrapper.get_version()
        # Get the version of the CLI and make sure it is correct
        assert None != result

    def test_get_version_with_out_binary(
        self,
    ) -> None:
        """
        Verify that GenericCliWrapper.get_version() raises exception CliCommandFailed
        when no binary set

        """
        GenericCliWrapper._SHELL_REQUIRED=False
        GenericCliWrapper._CLI_BINARY=None
        GenericCliWrapper._VERSION_ARGUMENT="--version"
        
        with pytest.raises(CliCommandFailed):
            result = GenericCliWrapper.get_version()
