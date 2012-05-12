import sys
import os
import logging

# Add script parent directory to python search path to get access to the evlio package
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

PRE_STR = ['#include <FITSRecord.hh>\n\nnamespace FR', ' {\n\n']

import evlio
import evlio.utils

import tpl2record

tpldict = evlio.utils.get_tpls_as_dict()

outfiles = []

for tplname, verdict in tpldict.iteritems() :
    for version, files in verdict.iteritems() :
        indextpl = evlio.BASE_PATH + '/templates/' + tplname + '/' + version + '/index.tpl'
        if os.path.isfile(indextpl) :
            outfile =  evlio.BASE_PATH + '/src/Records_' + tplname + '_' + version.replace('.','-') + '.hh'
            prestr = PRE_STR[0] + tplname.upper() + version.replace('.','') + PRE_STR[1]
            poststr = '}\n'
            tpl2record.tpl2record(indextpl, outfile, prestr, poststr)
            outfiles.append(outfile)
        else :
            logging.warning('Could not open index file ' + indextpl)
