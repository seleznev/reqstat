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
import logging as log

from reqstat.logentry import LogEntry

def parse_syslog_message(message):
    regex = re.compile("^\<[\d]+\>[\w]+ [\d]+ \d\d:\d\d:\d\d [\w]+ [\w]+: (?P<data>.*)$")

    r = re.search(regex, message.decode("utf-8"))
    if r:
        return r.group("data")
    else:
        raise ValueError("can't parse syslog message: {}".format(data))

def parse_entry(item, regex):
    log_regex = re.compile(regex)

    # Receive log message
    try:
        line = parse_syslog_message(item)
        entry = LogEntry(line, log_regex)
    except ValueError as e:
        log.error(e)
        entry = None

    return entry
