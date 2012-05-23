========
Overview
========

The purpose of the library is twofold:

1. It should provide tools to read, write, and verify data in CTA-EVL
format. Currently, this is implemented via FITSRecord (C++) but in
principal several different codes and programming languages can be
integrated. It should also provide extensive documentation and
examples how these libraries can be integrated in existing code.

2. The library should provide procedures and tools to automatically
manage updates of the data format and generate the relevant code. This
is currently implemented using `cfitsio FITS template files
<http://heasarc.gsfc.nasa.gov/docs/software/fitsio/c/c_user/node105.html>`_
and a custom python parser.

.. note::
    The current focus of evlio is on writing eventlist. Reading
    eventlists is implement in FITSRecord, but no convenience
    functions for, e.g., reading complete headers, are implemented yet.

----------------
Directory layout
----------------

The library is organized into several directories:

``templates/``
    The ``templates`` directory keeps the fitsio template
    files for the different formats and and versions, e.g.,
    ``templates/evl/1.0.0/`` keeps the templates for the eventlist
    format (``evl``) for version ``1.0.0``. The main template files
    from the parsing is started is called ``index.tpl``.

``evlio/``
    The ``evlio`` directory contains the python package for
    parsing fitsio templates.

``scripts/``
    The ``scripts`` folder contains executable pythons scripts that
    use routines from the ``evlio`` package to generate code, e.g.,
    data structs in header files for ``FITSRecord``.

``FITSRecord/``
    Source and header files for FITSRecord.

``docs/`` 
    The documentation is writen in `reStructured text format
    <http://sphinx.pocoo.org/rest.html#rst-primer>`_ and created using
    `sphinx <http://sphinx.pocoo.org>`_.

--------
Workflow
--------

1. Create templates in fitsio template format and add them to properly
   named subdirectories of the ``templates`` folder. Do not forget an
   ``index.tpl`` file.
2. Executed ``cmake``. This will

   1. generate the required includes using pythons scripts and
   2. compile the library
