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
import datetime

# Add script parent directory to python search path to get access to the evlio package
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import evlio
import evlio.utils

import tpl2record

RECORDS_STR = ('//\n// Create by evlio version ' + evlio.__version__ + '\n'
               + '// ' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '\n//\n\n')

PRE_STR = [
    RECORDS_STR + 
    '#include <FITSRecord.hh>\n\nnamespace ',
    ' {\n\n'
    ]

#===========================================================================
# Main

#---------------------------------------------------------------------------
def create_records(input_dir, output_dir, loglevel) :

    # Configure logging
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    if input_dir :
        input_dir = os.path.abspath(input_dir)
    if output_dir :
        output_dir = os.path.abspath(output_dir)

    tpldict = evlio.utils.get_tpls_as_dict(input_dir)

    recordstr= ''

    for tplname, verdict in tpldict.iteritems() :
        namespace = ''
        for version, files in verdict.iteritems() :
            indextpl = input_dir + '/' + tplname + '/' + version + '/index.tpl'
            if os.path.isfile(indextpl) :
                outfile = None
                if output_dir :
                    outfile = output_dir + '/' + 'Records_' + tplname + '_' + version.replace('.','-') + '.hh'
                namespace = 'FITSRec' + tplname.upper() + version.replace('.','')
                prestr = PRE_STR[0] + namespace + PRE_STR[1]
                poststr = '}\n'
                print indextpl
                tpl2record.tpl2record(indextpl, outfile, prestr, poststr)
                if outfile :
                    recordstr += ('// Template  : ' + tplname + '\n' +
                                  '// Version   : ' + version + '\n' +
                                  '// Full path : ' + outfile + '\n\n')
                    recordstr += '#include <' + os.path.basename(outfile) + '>\n'
            else :
                logging.warning('Could not open index file ' + indextpl)
        recordstr += '\nnamespace FITSRec' + tplname.upper() + 'Current = ' + namespace + ';\n\n'

    if output_dir :
        outfile = open(output_dir + '/Records.hh', 'w')
        outfile.write(RECORDS_STR + recordstr)
        outfile.close()

#---------------------------------------------------------------------------
if __name__ == '__main__' :
    # We should switch to argparse soon (python v2.7++)
    # http://docs.python.org/library/argparse.html#module-argparse
    import optparse
    parser = optparse.OptionParser(
        usage='%prog [options] <tpldir>',
        description='Converts fitsio tpl files into structs for FITSRecord.'
    )
    parser.add_option(
        '-o','--output-directory',
        dest='output_dir',
        type='str',
        default=None,
        help='Write output to directory [default: %default].'
    )
    parser.add_option(
        '-l','--log-level',
        dest='loglevel',
        default='INFO',
        help='Amount of logging e.g. DEBUG, INFO, WARNING, ERROR [default: %default]'
    )

    options, args = parser.parse_args()

    if len(args) == 1 :
        create_records(
            input_dir=args[0],
            output_dir=options.output_dir,
            loglevel=options.loglevel
            )
    else :
        parser.print_help()

#===========================================================================
#===========================================================================
