# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import re

from typing.re import Pattern

class LogEntry():
    def __init__(self, data, parser='regex', regex=None, container='syslog'):
        """Arguments:

        - data - source message (for ex. syslog message with log entry)
        - parser - parser type. Can be 'json' or 'regex'
        - regex - regex that will be used to parse line (for 'regex' parser)
        - container - type of container. Can be 'syslog' or None
        """

        # Unpack message
        if container == 'syslog':
            data = self._parse_syslog_message(data)
        elif container is None:
            pass # do nothing
        else:
            raise RuntimeError('LogEntry parser doesn\'t support "{}" container'.format(container))

        # Parse
        if parser == 'json':
            self.fields = json.loads(data)
        elif parser == 'regex':
            if isinstance(regex, Pattern):
                pass # regex already compiled - nothing to do
            elif isinstance(regex, str):
                regex = re.compile(regex)
            else:
                raise RuntimeError('regex type is not valid')

            self.fields = self._parse(data, regex)
        else:
            raise RuntimeError('LogEntry parser doesn\'t support "{}" parser'.format(parser))

    def items(self):
        return self.fields.items()

    def keys(self):
        return self.fields.keys()

    def __getitem__(self, key):
        if not key in self.fields:
            return None

        return self.fields[key]

    def __setitem__(self, key, item):
        self.fields[key] = item

    def __str__(self):
        return json.dumps(self.fields, indent=4, sort_keys=False)

    def _parse(self, line, regex):
        r = re.search(regex, line)
        if r:
            return r.groupdict()
        else:
            raise ValueError('can\'t parse log entry: {}'.format(line))

    def _parse_syslog_message(self, message):
        regex = re.compile('^\<[\d]+\>[\w]+ [\d]+ \d\d:\d\d:\d\d [^\s]+ [^\s]+: (?P<data>.*)$')

        r = re.search(regex, message.decode('utf-8'))
        if r:
            return r.group('data')
        else:
            raise ValueError('can\'t parse syslog message: {}'.format(message))
