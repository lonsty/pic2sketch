.. _getting_started:

.. toctree::
    :glob:

***************
Getting Started
***************

Installing the Library
======================

You can use pip to install `pic2sketch`.

.. code-block:: bash

    $ pip install pic2sketch

Usage
=====

Use `pic2sketch` to convert pictures to sketches in the terminal:

.. code-block:: bash

    p2sk < PIC | DIR > [ --include SYNTAX ] [ --exclude SYNTAX ] [ -s | --sigma INT] [ -d | --destination DIR ]

Examples
========

* Convert a picture to sketch:

.. code-block:: bash

    p2sk example.jpg

* Convert all pictures in a folder `photos/` to sketches, include filename has a word of `example`, exclude filename has a word of `sketch`, then save all the sketches to folder `new/`:

.. code-block:: bash

    p2sk photos/ --include "*example*" --exclude "*sketch*" -d new/