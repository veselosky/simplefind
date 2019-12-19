"""Implements the simplefind command line tool."""
import fnmatch
import os
import re
import shlex
import sys

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
    "--dotdirs/--no-dotdirs",
    "dotdirs",
    default=False,
    help="Also descend into dot directories like .git (skipped be default)",
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
@click.argument("frag", nargs=-1)
def find(
    any_logic=True,
    directory=["."],
    dotdirs=False,
    sep="\n",
    escape=True,
    use_case=False,
    frag=[],
):
    # Which logic type to use?
    collect = any
    if not any_logic:
        collect = all

    # Whether to shell-escape the output. We only apply shell escapes when
    # writing to a terminal, as escapes will not be interpreted by the shell
    # when piping output, and we don't want to write escaped versions when
    # redirecting to files.
    esc = lambda x: x
    if escape and sys.stdout.isatty():
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

    # If no pattern provided, mimic find and match all
    if not patterns:
        patterns.add("*")

    # search for files that match patterns
    the_matches = set()
    for adir in directory:
        for dirpath, dirnames, files in os.walk(adir):
            # Remove dotdirs like .git or .tox
            if not dotdirs:
                # Important to cast to list. Cannot modify dirnames while iterating.
                # donotdescend must therefore be a new list, not an iterator.
                donotdescend = list(filter(lambda x: x.startswith("."), dirnames))
                for d in donotdescend:
                    # dirnames is passed by ref, must be modified in place to
                    # affect walk
                    dirnames.remove(d)

            for fname in files:
                comp_name = fname
                if not use_case:
                    comp_name = fname.lower()
                if collect(fnmatch.fnmatch(comp_name, pat) for pat in patterns):
                    the_matches.add(os.path.join(dirpath, fname))

    # output in the requested format
    output = sep.join(esc(f) for f in sorted(the_matches))
    print(output)


if __name__ == "__main__":
    find()
