import subprocess as sub
import shlex
from typing import List, Optional, Tuple, Union


def run_command(cmd: str, timeout: Optional[float] = None, get_both_output_and_errors: bool = False, get_return_code: bool = False) -> Union[Tuple[str, str], Tuple[str, str, int]]:
    # Use shlex.split to properly handle quoted arguments
    args = shlex.split(cmd)

    # Execute the command and capture stdout and stderr
    result = sub.run(args, timeout=timeout, stdout=sub.PIPE, stderr=sub.PIPE, text=True)

    # Prepare the return values based on the flags
    if get_both_output_and_errors:
        if get_return_code:
            return result.stdout, result.stderr, result.returncode
        else:
            return result.stdout, result.stderr
    else:
        if get_return_code:
            if result.returncode == 0:
                return result.stdout, result.returncode
            else:
                return result.stderr, result.returncode
        else:
            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr


def run_commands(cmds: List[str], timeout: Optional[float] = None, get_both_output_and_errors: bool = False, get_return_code: bool = False) -> List[Union[Tuple[str, str], Tuple[str, str, int]]]:
    results = []

    for cmd in cmds:
        result = run_command(cmd, timeout, get_both_output_and_errors, get_return_code)
        results.append(result)

    return results


if __name__ == '__main__':
    # Linux only command, Might not run on windows.
    run_command('mkdir "Test World"')
