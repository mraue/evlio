========
Overview
========

The purpose of the library is twofold:

1. It should provide tools to read, write, and verify data in CTA-EVL format. Currently, this is implemented via FITSRecord (C++) but in principal several different codes and programming languages can be integrated. It should also provide extensive documentation and examples how these libraries can be integrated in existing code.

2. The library should provide procedures and tools to automatically manage updates of the data format. This is currently implemented using cfitsio FITS template files and a python parser.

----------------
Directory layout
----------------

The library is organized into several directories.

``templates/``
    The ``templates`` directory keep the fitsio template files for the different formats and and versions, e.g., ``templates/evl/1.0.0/`` keeps the templates for the eventlist format (``evl``) for version ``1.0.0``. The main template files from the parsing is started is called ``index.rst``.

``evlio/``
    The ``evlio`` keep the python package for parsing fitsio templates.

``scripts/``
    The ``scripts`` folder contains executable pythons scripts that use routines from the ``evlio`` package to create code, e.g., header files for ``FITSRecord``.

``src/``
    The actual C++ library code is kept in the ``src`` directory, in which on can also find the ``.o`` files and the library after compilation (tbc).
