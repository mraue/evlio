import sys
import os
import logging

# Add script parent directory to python search path to get access to the evlio package
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

PRE_STR = ['#include <FITSRecord.hh>\n\nnamespace ', ' {\n\n']

import evlio
import evlio.utils

import tpl2record

tpldict = evlio.utils.get_tpls_as_dict()

recordstr = ''

for tplname, verdict in tpldict.iteritems() :
    namespace = ''
    for version, files in verdict.iteritems() :
        indextpl = evlio.BASE_PATH + '/templates/' + tplname + '/' + version + '/index.tpl'
        if os.path.isfile(indextpl) :
            outfile = 'Records_' + tplname + '_' + version.replace('.','-') + '.hh'
            outpath = evlio.BASE_PATH + '/src/'
            namespace = 'FITSRec' + tplname.upper() + version.replace('.','')
            prestr = PRE_STR[0] + namespace + PRE_STR[1]
            poststr = '}\n'
            tpl2record.tpl2record(indextpl, outpath + outfile, prestr, poststr)
            recordstr += '// ' + tplname + ' ' + version + ' ' + outpath + outfile + '\n'
            recordstr += '#include <' + outfile + '>\n'
        else :
            logging.warning('Could not open index file ' + indextpl)
    recordstr += 'namespace FITSRec' + tplname.upper() + 'Current = ' + namespace + ';\n\n'

outfile = open(evlio.BASE_PATH + '/src/Records.hh', 'w')
outfile.write(recordstr)
outfile.close()
