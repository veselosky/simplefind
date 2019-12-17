"""Implements the simplefind command line tool."""
import fnmatch
import os
import re
import shlex

import click

WILDCARDS = re.compile(r"[\[\*\?]")


@click.command()
@click.option(
    "--any/--all",
    "-o/-a",
    "any_logic",
    default=True,
    help=(
        "When multiple fragments given, "
        "return files matching ANY fragment (OR logic, the default) "
        "or files matching ALL fragments (AND logic) "
    ),
)
@click.option(
    "--directory",
    "-d",
    multiple=True,
    type=click.Path(exists=True, file_okay=False, path_type=str),
    default=["."],
    help="Directory to search. Default = current directory. Can be given multiple times.",
)
@click.option(
    "--escape/--no-escape",
    "-e/-E",
    "escape",
    default=True,
    help="(default) Escape output for use as shell arguments",
)
@click.option(
    "-0",
    "sep",
    flag_value=chr(0),
    help="Output file names separated by NULLs (for xargs -0)",
)
@click.option(
    "-1", "sep", flag_value=" ", help="Output one line, file names separated by spaces"
)
@click.option(
    "-2",
    "sep",
    flag_value="\n",
    default=True,
    help="(default) Output each file name on a separate line",
)
@click.option("--case-sensitive/--case-insensitive", "-c/-i", "use_case", default=False)
@click.argument("frag", nargs=-1, required=True)
def find(any_logic, directory, sep, escape, use_case, frag):
    # Which logic type to use?
    comp = any
    if not any_logic:
        comp = all

    # Whether to shell-escape the output
    esc = lambda x: x
    if escape:
        esc = shlex.quote

    # Build the shell patterns to match against
    patterns = set()
    for fragment in frag:
        if not use_case:
            fragment = fragment.lower()
        if WILDCARDS.findall(fragment):  # the fragment has wildcards, pass through
            patterns.add(fragment)
        else:  # assume substring, add wildcards
            patterns.add(f"*{fragment}*")

    # search for files that match patterns
    the_matches = set()
    for dir in directory:
        for dirpath, dirnames, files in os.walk(dir):
            for fname in files:
                comp_name = fname
                if not use_case:
                    comp_name = fname.lower()
                if comp(fnmatch.fnmatch(comp_name, pat) for pat in patterns):
                    the_matches.add(os.path.join(dirpath, fname))

    # output in the requested format
    output = sep.join(esc(f) for f in the_matches)
    print(output)


if __name__ == "__main__":
    find()
