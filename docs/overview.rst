========
Overview
========

The purpose of the library is twofold:

1. The library should provide tools to read, write, and verify data in
   CTA-EVL format. Currently, this is implemented via :doc:`fitsrecord` (C++)
   but in principal several different codes and programming languages can
   be integrated. It should also provide extensive documentation and
   examples how these libraries can be integrated in existing code.
 
2. The library should provide procedures and tools to automatically
   manage updates of the eventlist data format and generate the relevant
   code. This is currently implemented using `cfitsio FITS template files
   <http://heasarc.gsfc.nasa.gov/docs/software/fitsio/c/c_user/node105.html>`_
   and a custom python parser and module called ``evlio``.

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
    `sphinx <http://sphinx.pocoo.org>`_. The documentation can also be
    found online under http://evlio.rtfd.org/ (hosted by http://readthedocs.org).
