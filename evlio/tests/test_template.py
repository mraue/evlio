#===========================================================================
# Copyright (c) 2012, the evlio developers
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the PyFACT developers nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
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

import os

from .. import template

PATH = os.path.dirname(os.path.abspath(__file__))

#===========================================================================
# Main

"""Unit tests for nosetest (http://nose.readthedocs.org/)"""

class TestFITSHeaderEntry() :
    """Test FITSHeaderEntry class"""

    def test_init(self) :
        fh = template.FITSHeaderEntry(key='key1', value='value1', comment='comment1')
        assert fh.key == 'key1'
        assert fh.value == 'value1'
        assert fh.comment == 'comment1'

    def test_parse_value(self) :
        fh = template.FITSHeaderEntry(value='1', parse_value=True)
        assert fh.value == 1
        fh = template.FITSHeaderEntry(value='.1', parse_value=True)
        assert fh.value == .1
        fh = template.FITSHeaderEntry(value='3E5', parse_value=True)
        assert fh.value == 3E5
        fh = template.FITSHeaderEntry(value='1.1.1', parse_value=True)
        assert fh.value == '1.1.1'

    def test_parse_extra_properties(self) :
        fh = template.FITSHeaderEntry(comment='comment1 {tt=tt}',
                                      parse_options=True)
        assert fh.comment == 'comment1'
        assert fh.options['tt'] == 'tt'
        fh = template.FITSHeaderEntry(comment='comment1 comment2 {t1=v1,t2=v2, t3=v3}',
                                      parse_options=True)
        assert fh.comment == 'comment1 comment2'
        assert fh.options['t1'] == 'v1'
        assert fh.options['t2'] == 'v2'
        assert fh.options['t3'] == 'v3'

class TestFITSExtension() :
    """Test FITSHeaderEntry class"""

    def test_init(self) :
        fh = template.FITSHeader([
            template.FITSHeaderEntry(key='EXTENSION', value='val1'),
            template.FITSHeaderEntry(key='EXTNAME', value='val2'),
            template.FITSHeaderEntry(key='BITPIX', value='val3'),
            template.FITSHeaderEntry(key='NAXIS', value='val4')
            ])
        fe = template.FITSExtension()
        fe.init_from_header(fh)
        assert fe.type_ == 'val1'
        assert fe.name == 'val2'
        assert fe.bitpix == 'val3'
        assert fe.naxis == 'val4'

class TestFITSFileTemplate() :
    """Test FITSFileTemplate class"""
    tpl = template.FITSFileTemplate(PATH + '/dummy.tpl', True)
    assert len(tpl.extensions) == 2
    assert len(tpl.extensions[1].header) == 63
    assert tpl.extensions[1].header[62].key == 'TUNIT20'
    assert tpl.extensions[1].header[62].value == 'TeV'
    assert tpl.extensions[1].header[1].options['mapto'] == 'v1'
    assert tpl.extensions[1].header[1].options['color'] == 'green'
    
#===========================================================================
#===========================================================================
