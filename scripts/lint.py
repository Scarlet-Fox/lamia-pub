import os
from pylint import lint
import yapf.yapflib.yapf_api as yapf


def main():
    """
    Tool for running all linting operations at once.

    Runs yapf in place on the codebase. Then fails out if pylint gives a score
    below a set threshold.
    """
    # Have to manually get each file to format, as the batch formatter in yapf
    # requires line numbers
    for path, _, files in os.walk("./lamia"):
        for file in files:
            if file[-3:] == ".py":
                fullpath = "{}/{}".format(path, file)
                yapf.FormatFile(fullpath, in_place=True, style_config=".yapfrc")

    pylint_results = lint.Run(['--rcfile', '.pylintrc', 'lamia'],
                              do_exit=False)
    if pylint_results.linter.stats['global_note'] < 7:
        print("Your pylint score was below a rating of 7.\n"
              "Be advised that this will likely cause any contrbutions that "
              "you have made to be delayed until the score can be raised. "
              "Possible changes that you can make include:\n\n"
              "Specify areas in the code where the lint errors can be ignored "
              "using `pylint: disable` comments.\n"
              "Correcting small mistakes that are hard to notice without linting, "
              "such as trailing whitespace.")


if __name__ == "__main__":
    main()
