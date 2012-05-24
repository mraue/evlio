#===========================================================================
# Copyright (c) 2012, the evlio developers
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the PyFACT developers nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE PYFACT DEVELOPERS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#===========================================================================
# Imports

import sys
import os
import logging
import re

# Add script parent directory to python search path to get access to the evlio package
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

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

#===========================================================================
# Regular expressions

TABLE_FORMAT_RE = re.compile(r'(?P<veclen>[0-9]+)?(?P<form>[ALXBSIUJVKEDCM]|A[0-9]+)')

#===========================================================================
# Dictionaries and constants

FITS_TABLE_FORMAT_TO_RECORD_TYPE = {'A': 'std::string', 'L': 'bool', 'X': 'bool',
                                    'B': 'unsigned char', 'S': 'char', 'I': 'short',
                                    'U': 'unsigned short', 'J': 'int', 'V': 'unsigned int',
                                    'K': 'long', 'E': 'float', 'D': 'double', }
EXCLUDE_FROM_HEADER = ['XTENSION', 'EXTNAME', 'EVTVER', 'COMMENT', 'HISTORY']
DATA_REC_STRUCT = [
    '  struct recdata_', ' {\n\n', '\n  };\n\n'
    ]
HEADER_REC_STRUCT = [
    '  struct recheader_', ' {\n\n', '\n  };\n\n'
    ]
WRITE_HEADER_STR = [
    '    void writeFullHeader() {\n\n', '\n    }\n\n'
    ]
READ_HEADER_STR = [
    '    void readFullHeader() {\n\n', '\n    }\n\n'
    ]
FITS_REC_STRUCT = [
    '  struct ',
    '''Record : public FITSRecord {

    ''',
    '''Record (std::string filename, std::string templatename)
      : FITSRecord( filename, templatename, "''','''" )  {\n\n''',
    '\n    }\n\n    recdata_', ' data;\n    recheader_', ' header;\n\n', '  };\n\n'
    ]

#===========================================================================
# Functions and classes

#---------------------------------------------------------------------------
def tpl2record(input_file, output_file=None, prestr='', poststr='', loglevel='INFO') :
    # Configure logging
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Open and parse FITS tpl file
    #t = evlio.template.FITSFileTemplate(evlio.BASE_PATH + '/templates/evl/1.0.0/EventList.tpl', True)
    t = evlio.template.FITSFileTemplate(input_file, True)

    outstream = sys.stdout
    if output_file :
        outstream = open(output_file, 'w')

    outstream.write(prestr)

    # Loop over extensions and print out FITSRecord structs
    ext_added = []
    for ext in t.extensions :
        # Better skip extensions of unknown type
        if ext.name == None :
            continue
        # Check if FITSRecord for extensions has already been created
        if ext.name in ext_added :
            logging.warning('Extension ' + ext.name + ' already added to FITSRecord. Skipping entry.')
            continue
        else :
            ext_added.append(ext.name)
        # Parse FITS header into FITSDataTables
        ext.data = evlio.template.FITSDataTable(ext.header, parse_options=True)
        # Loop over table columns
        if ext.data.columns :
            initstr, memberstr = '', ''
            for col in ext.data.columns :
                m = TABLE_FORMAT_RE.match(col.form)
                if (col.type_ and col.form and m and m.group('form') and
                    m.group('form') in FITS_TABLE_FORMAT_TO_RECORD_TYPE.keys()) :
                    initstr += ('      mapColumnToVar( "' + col.type_
                                + '" , data.' + col.type_.lower() + ' );\n')
                    memberstr += ('    ' + FITS_TABLE_FORMAT_TO_RECORD_TYPE[m.group('form')]
                                  + ' ' + col.type_.lower() + ';')
                    if col.unit or hasattr(col, 'comment') :
                        memberstr += ' // '
                    # Add unit as comment
                    if col.unit :
                        memberstr += '[' + col.unit + '] '
                    # Add comment from TTYPE header keyword
                    if hasattr(col, 'comment') :
                         memberstr += col.comment.strip()
                    memberstr += '\n'
                else :
                    logging.warning(
                        'Could not create record entry from column ' + col.type_
                        + ' in extension ' + ext.name
                        )
            headerrecstr, writeheaderstr, readheaderstr = '', '', ''
            # Create recheader struct
            for he in ext.header :
                if (not evlio.template._IS_TABLE_KW_RE.match(he.key) and
                    he.key.upper() not in EXCLUDE_FROM_HEADER) :
                    type_ = r'std::string'
                    if type(he.value) is float :
                        type_ = r'float'
                    elif type(he.value) is int :
                        type_ = r'int'
                    headerrecstr += ('    ' + type_ + ' ' + he.key.lower() + ';')
                    if he.comment :
                        headerrecstr += ' // ' + he.comment
                    headerrecstr += '\n'
                    writeheaderstr += ('      writeHeader( "' + he.key.upper() + '", header.' +
                                       he.key.lower() + ' );\n')
                    readheaderstr += ('      readHeader( "' + he.key.upper() + '", header.' +
                                      he.key.lower() + ' );\n')

            # Write structs to file
            outstream.write(DATA_REC_STRUCT[0] + ext.name.lower() + DATA_REC_STRUCT[1]
                            + memberstr + DATA_REC_STRUCT[2])
            outstream.write(HEADER_REC_STRUCT[0] + ext.name.lower() + HEADER_REC_STRUCT[1]
                            + headerrecstr + HEADER_REC_STRUCT[2])
            outstream.write(FITS_REC_STRUCT[0] + ext.name.upper() + FITS_REC_STRUCT[1]
                            + ext.name.upper()
                            + FITS_REC_STRUCT[2] + ext.name.upper() + FITS_REC_STRUCT[3] + initstr
                            + FITS_REC_STRUCT[4] + ext.name.lower() + FITS_REC_STRUCT[5]
                            + ext.name.lower() + FITS_REC_STRUCT[6]
                            + WRITE_HEADER_STR[0] + writeheaderstr + WRITE_HEADER_STR[1]
                            + READ_HEADER_STR[0] + readheaderstr + READ_HEADER_STR[1]
                            + FITS_REC_STRUCT[7])
    outstream.write(poststr)
    if output_file :
        outstream.close()
    return


#---------------------------------------------------------------------------
if __name__ == '__main__' :
    # We should switch to argparse soon (python v2.7++)
    # http://docs.python.org/library/argparse.html#module-argparse
    import optparse
    parser = optparse.OptionParser(
        usage='%prog [options] <tplfile>',
        description='Converts a fitsio tpl file into structs for FITSRecord.'
    )
    parser.add_option(
        '-o','--output-file',
        dest='output_file',
        type='str',
        default=None,
        help='Write output to file [default: %default].'
    )
    parser.add_option(
        '-l','--log-level',
        dest='loglevel',
        default='INFO',
        help='Amount of logging e.g. DEBUG, INFO, WARNING, ERROR [default: %default]'
    )

    options, args = parser.parse_args()

    if len(args) == 1 :
        tpl2record(
            input_file=args[0],
            output_file=options.output_file,
            loglevel=options.loglevel
            )
    else :
        parser.print_help()
    
#===========================================================================
#===========================================================================
