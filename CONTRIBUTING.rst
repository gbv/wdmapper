Contributing
=============

Feedback and contributions are very welcome!

This is my first Python project so I try to follow best-practice I could find.
Please let me know if I either missed something or if I was to pedandic!

Running from source
-------------------

You can manually execute wdmapper from source tree for testing:

.. code:: shell

    $ ./wdmapper.py

Issue tracker
-------------

Please report bugs and feature requests at
https://github.com/gbv/wdmapper/issues!

Development requirements
------------------------

Additional requirements for development are listed in ``dev-requirements.txt``.
Install via ``pip install -r dev-requirements.txt``.

Testing
-------

Please test functionality with unit tests, located in directory ``tests``.

.. code:: shell

    $ python setup.py test 
    $ pytest

Run a single test file:

.. code:: shell

    $ pytest tests/test\_whatever.py    

Test plugins and default options are configured in setup.cfg.

To run all tests with multiple versions of Python use
`tox <https://tox.readthedocs.io/>`_:

.. code:: shell
    
    $ tox

It is important to check with tox to ensure compatibility with both
Python 2.7 and Python 3.x. Which versions to test with and other options
are configured in ``tox.ini``.

Tests are also executed at https://travis-ci.org/gbv/wdmapper after
pushing commits to GitHub.
