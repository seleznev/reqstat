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
import copy
import logging as log
from collections import OrderedDict

from prometheus_client import Counter

from reqstat.logtransform import LogTransform

class LogStat():
    def __init__(self, config={}):
        self.metrics = {}

        # Create Prometheus metrics from config
        for m in config:
            name = m["name"]
            type = m["type"]

            help = ""
            if "help" in m:
                help = m["help"]

            labels = []
            transforms = []
            for f in m["fields"]:
                labels += [f["name"]]

                if "transform" in f:
                    transforms.append({
                        "name": f["transform"],
                        "options": {
                            "field": f["name"]
                        }
                    })

            if type == "counter":
                metric = Counter(name, help, labels)
            else:
                log.warning("can't create metric for type \"{}\"".format(m["type"]))
                continue

            self.metrics[name] = {
                "type": type,
                "metric": metric,
                "labels": labels,
                "transforms": transforms,
            }

    def insert(self, r_entry):
        transformers = LogTransform()

        for name, metric in self.metrics.items():
            entry = copy.deepcopy(r_entry) # we need a original entry for every iteraion

            for transform in metric["transforms"]:
                transformer = transformers[transform["name"]]
                entry = transformer(entry, transform["options"])

            labels = []
            for field in metric["labels"]:
                if not field in entry.keys():
                    log.warning("can't find \"{}\" field in log entry: {}".format(field, entry))
                    return None # TODO

                labels.append(entry[field])

            self.metrics[name]["metric"].labels(*labels).inc()
