==========
FITSRecord
==========

Class to facilitate writing to FITS binary tables that have already
been defined (via e.g. a template). 

Author: Karl Kosack <karl.kosack@cea.fr>

--------
Overview
--------

The set of methods mapColumnToVar() are defined to make it simple
to connect C variables to FITS column types with little chance of
making mistakes. Internally, some hidden C++ template and virtual
function trickery is used to store the mappings and use them to
write the FITS table.

Currently supported are single variables of various types (see
the set of functions called getFITSType()) a well as
fixed-length C-style arrays (e.g. float a[10]).  To add new
types, typically one needs only to add a new getFITSType()
function.

To write a binary FITS table, follow this procedure: 

* constuct a FITSRecord, (either from an open FITS file or
  giving the filename and template to use if the file doesn't exist)
* map your local variables to FITS columns using mapColumnToVar()
* loop over your data, setting the local variables appropriately,
  and calling write() for each data row
* when the FITSRecord goes out of scope (or is deleted), the file
  is automatically closed and writing finishes.

-------
Example
-------

.. code-block:: c++
 
   ...
 
   FITSRecord rec( "output.fits", "template.tpl", "EVENTS" );
   float energy;
   unsigned long eventID;
   double eventTime;
 
   rec.mapColumnToVar( "ENERGY", energy );    
   rec.mapColumnToVar( "EVENTID", eventID );    
   rec.mapColumnToVar( "TIME", eventTime );    
 
   for (int ii=0; ii < 50; ii++) {
 	   energy = 1.1;
 	   eventID = ii;
 	   eventTime = ii*0.001; 
 	   cout << rec << endl;        
 	   rec.write();
    }

   ...

.. a more complete example is shown in fitsrecordtest.cpp

\note rather than constructing a FITSRecord directly, you may just
generate a subclass and do all the column mapping in the
constructor.  

.. Warning::

   To use a string variable in a table, use a char[] array and map the
   column as follows (giving the fixed size of the field, which should
   match the template).::
     char value[30];
     strcpy( value, "A test" );
     rec.mapColumnToVar( "MYCOLUMN", value, 30 );
   
   Eventually this should be fixed to work
   properly with std::strings, but right now it does not.


