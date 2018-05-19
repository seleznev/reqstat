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
import logging as log

from collections import OrderedDict

from prometheus_client import Counter, Gauge

class LogStat():
    def __init__(self, config={}):
        self.metrics = {}

        # Create Prometheus metrics from config
        for m in config:
            name = m["name"]

            help = ""
            if "help" in m:
                help = m["help"]

            type = m["type"]
            if type != "counter":
                log.warning("can't create metric for type \"{}\"".format(m["type"]))
                continue

            labels = []
            transforms = {}
            for f in m["fields"]:
                labels += [f["name"]]

                if "transform" in f:
                    transforms[f["name"]] = f["transform"]
                else:
                    transforms[f["name"]] = None

            self.metrics[name] = {
                "type": type,
                "metric": Counter(name, help, labels),
                "labels": labels,
                "transforms": transforms,
            }

    def insert(self, entry):
        for name, metric in self.metrics.items():
            labels = []
            for field in metric["labels"]:
                if not field in entry.keys():
                    log.warning("can't find \"{}\" field in log entry: {}".format(field, entry))
                    return None # TODO

                value = entry[field]
                if field in metric["transforms"]:
                    if metric["transforms"][field] == "http-code":
                        value = LogStat.get_key(value)

                labels.append(value)

            self.metrics[name]["metric"].labels(*labels).inc()

    @staticmethod
    def get_key(status):
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
