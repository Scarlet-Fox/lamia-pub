#!/usr/bin/env python
import subprocess
import sys
import os
import argparse

from pylint import lint
import yapf.yapflib.yapf_api as yapf


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--type",
        help="Type to be run, if not specified, a full lint is performed.",
        type=str,
        choices=["yaml", "lint"])
    parser.add_argument(
        "-c",
        "--changed-only",
        help="If set, uses git to discover and lint only uncommitted files",
        action="store_true")
    parser.add_argument(
        "Path",
        help="Path to be linted, defaults to entire project",
        type=str,
        nargs="?",
        default="./lamia")
    return parser.parse_args()


def main():
    """
    Tool for running all linting operations at once.

    Runs yapf in place on the codebase. Then fails out if pylint gives a score
    below a set threshold.
    """
    args = get_args()

    filepaths = []
    for directory, _, files in os.walk(args.Path):
        filepaths.extend([
            os.path.join(directory, file) for file in files
            if file[-3:] == ".py"
        ])

    if args.changed_only:
        # Disgusting but im not adding a depends for this
        filepaths = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True).stdout.decode().split()
    # Have to manually get each file to format, as the batch formatter in yapf
    # requires line numbers
    for filepath in filepaths:
        yapf.FormatFile(filepath, in_place=True, style_config=".yapfrc")

    pylint_results = lint.Run(
        ['--rcfile', '.pylintrc'] + filepaths, do_exit=False)
    if pylint_results.linter.stats['global_note'] < 7:
        print(
            "Your pylint score was below a rating of 7.\n"
            "Be advised that this will likely cause any contrbutions that "
            "you have made to be delayed until the score can be raised. "
            "Possible changes that you can make include:\n\n"
            "Specify areas in the code where the lint errors can be ignored "
            "using `pylint: disable` comments.\n"
            "Correcting small mistakes that are hard to notice without linting, "
            "such as trailing whitespace.")


if __name__ == "__main__":
    main()
