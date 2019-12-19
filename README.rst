simplefind
==========
simplefind is a simple tool for finding files. I created it because I
am *really* lazy and got tired of typing the same long set of find command
patterns.

* Using find: ``find . -not -path '*.git/*' -iname '*SUBSTRING*' -o -iname '*ALTSTRING*'``
* Using simplefind: ``ff SUBSTRING ALTSTRING``

USAGE
=====

Usage::

  ff [OPTIONS] [FRAG]...

Options::

  -o, --any / -a, --all           When multiple fragments given, return files
                                  matching ANY fragment (OR logic, the
                                  default) or files matching ALL fragments
                                  (AND logic)
  -d, --directory DIRECTORY       Directory to search. Default = current
                                  directory. Can be given multiple times.
  --dotdirs / --no-dotdirs        Also descend into dot directories like .git
                                  (skipped be default)
  -e, --escape / -E, --no-escape  (default) Escape output for use as shell
                                  arguments
  -0                              Output file names separated by NULLs (for
                                  xargs -0)
  -1                              Output one line, file names separated by
                                  spaces
  -2                              (default) Output each file name on a
                                  separate line
  -c, --case-sensitive / -i, --case-insensitive
  --help                          Show this message and exit.

Matches are case-insensitive by default. On Windows, matches will be
case-insensitive regardless because that's how Windows works.

> ff NAME
> ./.namedots.txt
> ./NAME.txt
> './name with spaces.txt'
> './name(parens).txt'

> ff -c NAME
> ./NAME.txt

When multiple FRAGs are given, the default behavior is to expand the search,
not narrow it.

> ff .jpg .gif # finds pictures matching either
> ./test1.jpg
> ./test2.gif

To narrow the search, use --all (a filename must match ALL FRAGs).

> ff -a .jpg test
> ./test1.jpg # but NOT test2.gif

When output is to a terminal, it is shell escaped by default, making it easy
to copy the output as arguments to other commands.

> ff NAME
> ./.namedots.txt
> ./NAME.txt
> './name with spaces.txt'
> './name(parens).txt'

To disable this, use -E.

> ff -E NAME
> ./.namedots.txt
> ./NAME.txt
> ./name with spaces.txt
> ./name(parens).txt

If you are piping the output to another program or redirecting to a file,
the output is not escaped.

> ff -d "$PWD" .mp3 > playlist.m3u # no shell escapes are applied

To pass the output as arguments to another program, use xargs.

> ff .txt | xargs edit # edit all the text files at once
