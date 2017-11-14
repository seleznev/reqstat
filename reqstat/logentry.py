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

import re

class LogEntry():
    def __init__(self, line, regex):
        self.fields = self._parse(line, regex)

    def items(self):
        return self.fields.items()

    def __getitem__(self, key):
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
            raise ValueError("can't parse log entry: {}".format(line))
