What is **pywrap**
==================

It is a generic command line wrapper for Python. It translates various python constructs
to their command line equivalents which means that it is limited in certain aspects where
the python language offers no equivalent construct.

Usage
=====

**pywrap** can be used to wrap around any command line tool. Let's
see an example with our favourite vcs `git`

.. code:: python

   from pywrap import Command
   git = Command('git') # Create wrapper


- `git(help=True)` will be translated to `git --help`
- `git.commit(message='My commit message')` will be translated to `git commit --message 'My commit message'`
- `git.push('origin', 'development')` will be translated to `git push origin master`

Overview
========

- attribute lookup are translated to sub-commands.
- keyword arguments are translated to flags. Both short and long form are supported.
- positional arguments are translated to well, positional arguments.
- `True` and `None` can be used as values for keyword arguments when the underlying flags takes no parameters.

Some things to Note
===================

- This project is in very early stagea. It will be someday on PyPI. can't say when.
- It is usual to have command line parameters to contain a `-`. Since a variable cannot have `-` in python, An `_` is translated to a `-`. You can escape
  this behaviour with another `_`.
- It is obvious that the **Command** objects would not provide docstrings. The calls are directly translated to command line statements. No validation is
  performed.

Contribute
==========

Please submit any issues or Feature requests in the issue tracker. PR's are most welcome.

License
=======

TODO  


