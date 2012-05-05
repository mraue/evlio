import sys
import os
import logging
import re

# Add script parent directory to python search path to get access to the evlio package
sys.path.append(os.path.abspath(sys.path[0].rsplit('/', 1)[0]))
import evlio
import evlio.template

# http://heasarc.gsfc.nasa.gov/docs/software/fitsio/quick/node10.html
#
#        Binary Table Column Format Codes
#        --------------------------------
#        (r = vector length, default = 1)
#            rA  - character string
#            rAw - array of strings, each of length w
#            rL  - logical
#            rX  - bit
#            rB  - unsigned byte
#            rS  - signed byte **
#            rI  - signed 16-bit integer
#            rU  - unsigned 16-bit integer **
#            rJ  - signed 32-bit integer
#            rV  - unsigned 32-bit integer **
#            rK  - 64-bit integer ***
#            rE  - 32-bit floating point
#            rD  - 64-bit floating point
#            rC  - 32-bit complex pair
#            rM  - 64-bit complex pair
#
#     ** The S, U and V format codes are not actual legal TFORMn values.
#        CFITSIO substitutes the somewhat more complicated set of
#        keywords that are used to represent unsigned integers or
#        signed bytes.
#
#    *** The 64-bit integer format is experimental and is not 
#        officially recognized in the FITS Standard.
#        
TABLE_FORMAT_RE = re.compile(r'(?P<veclen>[0-9]+)?(?P<form>[ALXBSIUJVKEDCM]|A[0-9]+)')

FITS_TABLE_FORMAT_TO_RECORD_TYPE = {'A': 'std::string', 'L': 'bool', 'X': 'bool',
                                    'B': 'unsigned char', 'S': 'char', 'I': 'short',
                                    'U': 'unsigned short', 'J': 'int', 'V': 'unsigned int',
                                    'K': 'long', 'E': 'float', 'D': 'double', }

RECORD_STRUCT_BEGIN = '''
  struct {0}FITSRecord : public FITSRecord {{

    EventListFITSRecord(std::string filename, std::string templatename, int ntels=256)
      : FITSRecord( filename, templatename, "{0}" ), nTels(ntels)
    {{

      setVerbose(1);
'''
RECORD_STRUCT_END = '''
    }
'''
RECORD_STRUCT_COL_ENTRY =  '''      mapColumnToVar( "{0}", {1} );
      {2} {1};'''
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

t = evlio.template.FITSFileTemplate(evlio.BASE_PATH + '/templates/v1.0.0/EventList.tpl', True)

for ext in t.extensions :
    if ext.name == None :
        continue
    ext.data = evlio.template.FITSDataTable(ext.header)
    if ext.data.columns :
        print RECORD_STRUCT_BEGIN.format(ext.name)
        for col in ext.data.columns :
            m = TABLE_FORMAT_RE.match(col.form)
            if (col.type_ and col.form and m and m.group('form') and
                m.group('form') in FITS_TABLE_FORMAT_TO_RECORD_TYPE.keys()) :
                print RECORD_STRUCT_COL_ENTRY.format(col.type_, col.type_.lower(),
                                                     FITS_TABLE_FORMAT_TO_RECORD_TYPE[m.group('form')])
            else :
                logging.warning('Could not create record entry from column {0} in extension {1}'.format(col.type_, ext.name))
        print RECORD_STRUCT_END

#    for he in ext.header :
#        if not evlio.template._IS_TABLE_KW_RE.match(he.key) :
#            type_ = r'char*'
#            if type(he.value) is float :
#                type_ = r'float'
#            elif type(he.value) is int :
#                type_ = r'int'
#            print type_, he.key.lower(), ';'
