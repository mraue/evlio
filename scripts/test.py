import sys
import os
import logging

# Add script parent directory to python search path to get access to the evlio package
sys.path.append(os.path.abspath(sys.path[0].rsplit('/', 1)[0]))
import evlio
import evlio.template

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

t = evlio.template.FITSFileTemplate(evlio.BASE_PATH + '/templates/evl/1.0.0/EventList.tpl', True)

for ext in t.extensions :
    logging.info('--------------------------------------------------------------------')
    logging.info('Found extension name={0} type={1}'.format(ext.name, ext.type_))
    for he in ext.header :
        logging.info('{0:>8} = {1:<20} / {2}'.format(he.key, he.value, he.comment))
    ext.data = evlio.template.FITSDataTable(t.extensions[1].header)
