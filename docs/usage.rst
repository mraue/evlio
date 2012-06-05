=======
Usage
=======

There are two main use cases:

**End user**
    The end user wants to write (or read) data in eventlist format using an already existing program/code. He/She will use the compiled library and header files and integrate them into the existing code. This is the main use case described below.

**Format keeper**
    This user implements a format update or a adds new format to the ``evlio`` framework. She/He will create `cfitsio FITS template files <http://heasarc.gsfc.nasa.gov/docs/software/fitsio/c/c_user/node105.html>`_ corresponding to the format definition and will add them to the ``templates`` directory.

-------------------------------------------
Writing eventlists using FITSRecord
-------------------------------------------

1.  First, the record include files need to be generated and the
    FITSRecord library needs to be compiled following the instructions in
    the :doc:`installation` section.
2.  To use FITSRecord with existing codes the appropriate library and
    include paths need to be added when building the code (also described
    in the :doc:`installation` section).

FITSRecord provide data structures (structs) which are mapped to a
fits output file. The data is organized in FITS extensions with one
struct per header and table data per extension. The different formats
and format versions are kept in separate namespaces following the
convention ``<TPL><VERSION>Records``, e.g., ``EVL100Records`` for the
evl (eventlist) template version 1.0.0.

For each pre defined FITS extension an FITSRecord class derived from
the base FITSRecord exists. E.g. for the EVENTS extension there is the
``EVENTSRecord`` class. The class has a ``header`` and a ``data``
member, which map to the corresponding header and table data structs,
respectively.

To write the data to a file, the ``write()`` and the
``writeFullHeader()`` are called for the table data and the header,
respectively.

Several definitions are provided in the central ``Records.hh`` file
and the specfic record files. In particular, definitions for the
namespace of the most recent version of a specific template are
defined, e.g., ``FITSRecEVLCurrent`` for the most recent version of
the eventlist template.

.. code-block:: c++

   #include <FITSRecord.hh>
   #include <Records.hh>

   ...

   // Create FITSRecord for a specific extension
   // (here EVENTS extension of an eventlist file)

   EVLRecordsCurrent::EVENTSRecord eventsrec( "output.fits", EVLRecordsCurrent::EVENTLIST_FILE_TPL);

   // Write header data
   // Please refer to the corresponding Record_<tpl>_<version>.hh file
   // for more details on the possible entries and entry formats
   eventsrec.readFullHeader(); // Read previous or default values from file
   eventsrec.header.telescop = "MAGIC";
   eventsrec.header.date_obs = "2008-03-23";   
   ...
   eventsrec.writeFullHeader();

   loop over your events {
           // Fill data row with event data
           eventsrec.data.event_id = ..
           eventsrec.data.time = ..
           eventsrec.data.ra = ..
           eventsrec.data.dec = ..
           ...
          // Write data row
 	   eventsrec.write();
    }

   ...
