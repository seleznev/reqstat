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

import unittest

from reqstat.logentry import LogEntry

class TestLogEntry(unittest.TestCase):

    def test_parse(self):
        le = LogEntry('', parser='regex', regex='', container=None)

        self.assertEqual(le._parse('1 2 3', parser='regex', regex='^(?P<a>\d) (?P<b>\d) (?P<c>\d)$'),
                         {'a': '1', 'b': '2', 'c': '3'})

        self.assertEqual(le._parse('{"a": "1", "b": "2", "c": "3"}', parser='json'),
                         {'a': '1', 'b': '2', 'c': '3'})

        with self.assertRaises(ValueError):
            le._parse('1 2', parser='regex', regex='^\d$')

if __name__ == '__main__':
    unittest.main()