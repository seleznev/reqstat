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

LOG_FORMAT = re.compile(
    "^(?P<remote_addr>[a-f\d:.]+) - (?P<remote_user>[^\s]+) "\
    "\[(?P<time_local>[^\s]+ [^\s]+)\] "\
    "\"(?P<request_method>[A-Z_]+) (?P<request_uri>[^\"]+) HTTP/[^\"]+\" "\
    "(?P<status>[\d]+) (?P<body_bytes_sent>[\d]+) "\
    "\"(?P<http_referer>[^\"]*)\" \"(?P<http_user_agent>.*)\"$"
)

class LogProcessor():

    @staticmethod
    def get_key(status):
        if status >= 200 and status <= 299:
            return "2XX"
        elif status >= 300 and status <= 399:
            return "3XX"
        elif status >= 400 and status < 499:
            return "4XX"
        elif status == 499:
            return "499"
        elif status >= 500 and status <= 599:
            return "5XX"
        else:
            return "unknown"

    @staticmethod
    def parse_log_entry(line):
        r = re.search(LOG_FORMAT, line)
        if r:
            return {
                "status": int(r.group("status"))
            }
        else:
            raise ValueError("parsing error: {}".format(line))

    @staticmethod
    def process_queue(queue, messages_type="syslog"):
        stats = {
            "2XX": 0,
            "3XX": 0,
            "4XX": 0,
            "499": 0,
            "5XX": 0,
            "unknown": 0,
            "total": 0
        }

        while True:
            item = queue.get()

            if item is None:
                break

            try:
                if messages_type == "syslog":
                    r = re.search(re.compile("^\<[\d]+\>[\w]+ [\d]+ \d\d:\d\d:\d\d [\w]+ [\w]+: (?P<line>.*)$"),
                                  item.decode("utf-8"))
                    if r:
                        line = r.group("line")
                    else:
                        raise ValueError("parsing error: {}".format(item))
                else:
                    line = item

                result = LogProcessor.parse_log_entry(line)
            except ValueError as e:
                #print_error(str(e))
                break

            stats[LogProcessor.get_key(result["status"])] += 1
            stats["total"] += 1

            queue.task_done()

        return stats;

