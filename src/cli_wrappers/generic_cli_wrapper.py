#!/usr/bin/env python3

import logging
import subprocess
import typing as t


# The global logger used in this module
_logger = logging.getLogger(__name__)

class CliCommandFailed(Exception):
    """
    Thrown if the given CLI command returned an error.
    """
    pass

class GenericCliWrapper():
    """
    The generic singleton class used for executing commands
    through a specific CLI. The exact specifics of the CLI
    should be defined in the derived class by overriding
    class variables defined in this class.
    """

    _CLI_BINARY: t.ClassVar[str] = t.cast(str, None)
    """
    The name of the CLI binary.
    """

    _VERSION_ARGUMENT: t.ClassVar[str] = t.cast(str, None)
    """
    The command line argument to print the version information.
    """

    _SHELL_REQUIRED: t.ClassVar[bool] = False

    """
    Indicates whether a shell is required for executing the CLI binary.
    """

    @classmethod
    def get_version(cls) -> str:
        """
        Retrieves the version of the CLI binary installed.

        :return: The version of the CLI binary (may be a multi-line
                 string depending on the CLI behavior)
        :rtype: str

        :raises CliCommandFailed: If the CLI returned an error code
        """

        # Run the CLI with the correct version option
        return cls._run_cli(
            [cls._VERSION_ARGUMENT],
            log_output=False,  # The caller will log the version, if required
        ).strip()


    @classmethod
    def _run_cli(
        cls,
        args: t.List[str],
        log_output: bool = True,
    ) -> str:
        """
        Runs the CLI with the given arguments.

        :param args: The list of arguments for the CLI (not including
                     the name of the CLI binary itself)
        :type args: List[str]

        :param log_output: Indicates whether to log the output or not
        :type log_output: bool

        :return: The output produced by the CLI binary
        :rtype: str

        :raises CliCommandFailed: If the CLI returned an error code
        """

        # Log the command to be executed
        if cls._CLI_BINARY is None :
            _logger.error(
                "_CLI_BINARY is not set"
            )
            raise CliCommandFailed(
                "_CLI_BINARY is not set"
            )

        cli_command = [cls._CLI_BINARY] + args
        cli_command_str = " ".join(cli_command)

        _logger.info(
            "Executing {} CLI: {}".format(
                cls._CLI_BINARY,
                cli_command_str,
            ),
        )

        # Run the CLI with the given arguments
        result = subprocess.run(
            cli_command,
            stdout=subprocess.PIPE,     # Capture the output
            stderr=subprocess.STDOUT,   # Redirect stderr to stdout
            shell=cls._SHELL_REQUIRED,  # Some CLIs (gcloud) require a shell
        )

        # Check, if the CLI failed
        decoded_output: str = result.stdout.decode("utf-8")

        if result.returncode != 0:
            # The CLI failed, log the output, just in case
            _logger.error(
                "Unable to execute {} CLI ({}), error={}\n{}".format(
                    cls._CLI_BINARY,
                    cli_command_str,
                    result.returncode,
                    decoded_output,
                ),
            )
            raise CliCommandFailed(
                "Unable to execute {} CLI, error={}".format(
                    cls._CLI_BINARY,
                    result.returncode,
                ),
            )

        # The command executed successfully, log the output
        
        if log_output:
            _logger.info(
                "{} CLI ({}) executed successfully:\n{}".format(
                    cls._CLI_BINARY,
                    cli_command_str,
                    decoded_output,
                ),
            )
        else:
            _logger.info(
                "{} CLI ({}) executed successfully".format(
                    cls._CLI_BINARY,
                    cli_command_str,
                ),
            )

        return decoded_output