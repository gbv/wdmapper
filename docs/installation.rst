Installation
============

wdmapper requires Python 2.7 or higher. Releases can be installed from the
command line with `pip <https://pip.pypa.io/>`__:

.. code:: shell

    $ pip install wdmapper              # either install global
    $ pip install wdmapper --user       # or install to ~/.local

Add option `--user` to install as normal user to `~/.local` and option
`--upgrade` to update an already installed version.

The latest developer version can be retrieved from the git repository:

.. code:: shell

    $ git clone https://github.com/gbv/wdmapper.git
    $ cd wdmapper
    $ git checkout dev
    $ pip install -r requirements.txt
    $ ./wdmapper.py

