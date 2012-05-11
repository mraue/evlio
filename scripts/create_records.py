import sys
import os
import logging

# Add script parent directory to python search path to get access to the evlio package
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import evlio
import evlio.utils

import tpl2record

tpldict = evlio.utils.get_tpls_as_dict()

outfiles = []

for tplname, verdict in tpldict.iteritems() :
    for version, files in verdict.iteritems() :
        indextpl = evlio.BASE_PATH + '/templates/' + tplname + '/' + version + '/index.tpl'
        if os.path.isfile(indextpl) :
            outfile =  evlio.BASE_PATH + '/src/Records_' + tplname + '-' + version.replace('.','-') + '.hh'
            tpl2record.tpl2record(indextpl, outfile)
            outfiles.append(outfile)
        else :
            logging.warning('Could not open index file ' + indextpl)
