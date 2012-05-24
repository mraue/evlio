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
import glob
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
def create_records(tpl_dir, output_dir, loglevel) :

    # Configure logging
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    tpl_dir = os.path.abspath(tpl_dir)
    if output_dir :
        output_dir = os.path.abspath(output_dir)

    # Parse template directory structure
    tpldict = evlio.utils.get_tpls_as_dict(tpl_dir)

    recordstr= ''

    for tplname, verdict in tpldict.iteritems() :
        namespace = ''
        for version, files in verdict.iteritems() :
            indir = tpl_dir + '/' + tplname + '/' + version
            indextpl = indir + '/index.tpl'
            if os.path.isfile(indextpl) :
                outfile = None
                if output_dir :
                    outfile = output_dir + '/' + 'Record_' + tplname + '_' + version.replace('.','_') + '.hh'
                namespace = tplname.upper() + version.replace('.','') + 'Records'
                prestr = PRE_STR[0] + namespace + PRE_STR[1]
                # Add links to file templates (<xx>.file.tpl)
                tplfiles = glob.glob(indir + '/*.file.tpl')
                if tplfiles :
                    for f in tplfiles :
                        dir_, file_ = os.path.split(f)
                        id_ = file_.split('.')[0]
                        prestr += '  const std::string ' + id_.upper() + '_FILE_TPL(\'' + f + '\');\n'
                    prestr += '\n'
                poststr = '}\n'
                tpl2record.tpl2record(indextpl, outfile, prestr, poststr)
                if outfile :
                    recordstr += ('// Template    : ' + tplname + '\n' +
                                  '// Version     : ' + version + '\n' +
                                  '// Record file : ' + outfile + '\n\n')
                    recordstr += '#include <' + os.path.basename(outfile) + '>\n\n'
            else :
                logging.warning('Could not find index file in ' + indir)
        recordstr += 'namespace ' + tplname.upper() + 'RecordsCurrent = ' + namespace + ';\n\n'

    if output_dir :
        # Write central Records.hh file
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
            tpl_dir=args[0],
            output_dir=options.output_dir,
            loglevel=options.loglevel
            )
    else :
        parser.print_help()

#===========================================================================
#===========================================================================
