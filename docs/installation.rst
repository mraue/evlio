============
Installation
============

---------------
Obtaining evlio
---------------

The easiest way to obtain evlio is by cloning the repository via git::

    $ git clone git://github.com/mraue/evlio.git

You can also download the repository as tar or zip archive::

    $ wget https://github.com/mraue/evlio/tarball/develop

or via the download link from the webpage https://github.com/mraue/evlio/downloads.

-----------------------------
Code generation and compiling
-----------------------------

evlio is made using `cmake <http://www.cmake.org/>`_. cmake is best
employed from a separate ``build`` directory::

    $ mkdir build
    $ cd build
    $ cmake ..
    $ make

This creates all necessary Makefiles, runs the python code generator,
and compiles the FITSRecord library.

cmake will attempt to locate your installation of cfitsio. In case it
is installed in a custom location you have to set `CFITSIO_ROOT_DIR`
variable in the central `CMakeLists.txt` file to the path to your
installation, e.g., ::

    set(CFITSIO_ROOT_DIR /Users/mraue/Stuff/unix/cfitsio)

The build products (i.e. libraries & includes) will be located in
subdirectories of the ``build/`` directory.

To clear the installation, remove the content of the ``build/``
directory::

    $ cd build/
    $ rm -r *

To make the library word with your code you need to add the
``build/lib`` path to your library path and the ``build/include`` and
``build/records`` paths to your include path.
