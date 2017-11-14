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

from collections import OrderedDict

class LogStat():
    def __init__(self, metrics={}):
        self.stats = OrderedDict()
        self.metrics_fields = list(map(lambda m: m["field"], metrics))

    def insert(self, entry):
        for k,v in entry.items():
            if not k in self.metrics_fields:
                continue

            if not k in self.stats:
                self.stats[k] = {}

            if not str(entry[k]) in self.stats[k]:
                self.stats[k][str(entry[k])] = 0

            self.stats[k][str(entry[k])] += 1

    @staticmethod
    def merge_stats(*stats):
        result = LogStat()

        for s in list(stats):
            for k,v in s.stats.items():
                if not k in result.stats:
                    result.stats[k] = {}

                for kk,vv in v.items():
                    if not kk in result.stats[k]:
                        result.stats[k][kk] = 0

                    result.stats[k][kk] += s.stats[k][kk]

        return result

    def __str__(self):
        return json.dumps(self.stats, indent=4, sort_keys=False)

    def get_key(self, status):
        status = int(status)

        if status >= 200 and status <= 299:
            return "2XX"
        elif status >= 300 and status <= 399:
            return "3XX"
        elif status >= 400 and status <= 499:
            return "4XX"
        elif status >= 500 and status <= 599:
            return "5XX"
        else:
            return "unknown"
