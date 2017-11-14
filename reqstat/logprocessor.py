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
import socket
import logging as log

from reqstat.logentry import LogEntry
from reqstat.logstat import LogStat

class LogProcessor():
    @staticmethod
    def parse_syslog_message(message, regex):
        r = re.search(regex, message.decode("utf-8"))
        if r:
            return r.group("data")
        else:
            raise ValueError("can't parse syslog message: {}".format(data))

    @staticmethod
    def process_queue(queue, input={}, metrics=[]):
        stats = LogStat(metrics)

        syslog_regex = re.compile("^\<[\d]+\>[\w]+ [\d]+ \d\d:\d\d:\d\d [\w]+ [\w]+: (?P<data>.*)$")
        log_regex = re.compile(input["regex"])

        while True:
            item = queue.get()

            if item is None:
                break # interprets as shutdown worker command

            # Receive log message
            try:
                if input["type"] == "syslog":
                    line = LogProcessor.parse_syslog_message(item, syslog_regex)
                else:
                    line = item

                entry = LogEntry(line, log_regex)
            except ValueError as e:
                log.error(e)
                continue # skip this iteration

            # Insert into statistics
            stats.insert(entry)

            # Message processed successfully
            queue.task_done()

        return stats

    @staticmethod
    def receive_messages(queue, ip=None, port=None):
        network = (ip and port)

        if network:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 100*1024)
            sock.bind((ip, port))

        try:
            while True:
                if network:
                    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                else:
                    data = input() # from stdin
                queue.put(data)

        except (EOFError, KeyboardInterrupt):
            pass

