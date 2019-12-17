simplefind
==========
simplefind is a simple tool for finding files. I created it because I
am *really* lazy and got tired of typing the same long set of find command
patterns.

* Using find: ``find . -iname '*SUBSTRING*' -o -iname '*ALTSTRING*'``
* Using simplefind: ``ff SUBSTRING ALTSTRING``

The output is shell escaped by default, making it easy to use the output as
arguments to other commands.
