#!/usr/bin/env python
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2017-09-22 15:45:06 +0200 (Fri, 22 Sep 2017)
#
#  https://github.com/harisekhon/nagios-plugins
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/harisekhon
#

"""

Nagios Plugin to check the configured environment of a Presto SQL node

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import sys
import traceback
srcdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(srcdir, 'pylib')
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon.utils import validate_regex
    from harisekhon import RestNagiosPlugin
except ImportError as _:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.1'


class CheckPrestoEnvironment(RestNagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckPrestoEnvironment, self).__init__()
        # Python 3.x
        # super().__init__()
        self.host = None
        self.port = None
        self.auth = False
        self.json = True
        self.path = '/v1/service/presto/general'
        self.msg = 'Presto SQL node environment = '
        self.expected = None

    def add_options(self):
        self.add_hostoption(name='Presto', default_host='localhost', default_port=8080)
        self.add_ssl_option()
        self.add_opt('-e', '--expected', help='Expected environment setting (regex)')

    def process_options(self):
        super(CheckPrestoEnvironment, self).process_options()
        self.expected = self.get_opt('expected')
        if self.expected:
            validate_regex(self.expected, 'expected environment')

    def parse_json(self, json_data):
        environment = json_data['environment']
        self.msg += "'{0}'".format(environment)
        if self.expected and not re.match(self.expected + '$', environment):
            self.critical()
            self.msg += " (expected '{0}')".format(self.expected)


if __name__ == '__main__':
    CheckPrestoEnvironment().main()