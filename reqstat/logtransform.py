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

import logging as log

class LogTransform():
    def __getitem__(self, key):

        if key == "http-code":
            return self.http_code

        return self.blank

    @staticmethod
    def blank(entry, options={}):
        return entry

    @staticmethod
    def http_code(entry, options={}):
        if not "field" in options:
            log.warning("http-code transformer requires \"field\" option")
            return entry

        status = int(entry[options["field"]])

        if status >= 100 and status <= 199:
            status = "1XX"
        elif status >= 200 and status <= 299:
            status = "2XX"
        elif status >= 300 and status <= 399:
            status = "3XX"
        elif status >= 400 and status <= 499:
            status = "4XX"
        elif status >= 500 and status <= 599:
            status = "5XX"
        else:
            status = "unknown"

        entry[options["field"]] = status

        return entry
