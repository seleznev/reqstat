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

import sys
import yaml

class ConfigError(RuntimeError):
    def __init__(self, message, details=None):
        self.message = message
        self.details = details

    def __str__(self):
        return self.message

def load(path="reqstat.yml"):
    config = None
    try:
        with open(path, "r") as config_file:
            config = yaml.load(config_file)
    except IOError as e: # FileNotFoundError
        raise ConfigError("config not found: {}".format(path))
    except ValueError as e:
        raise ConfigError("parse config error: {}".format(str(e)))

    config = validate(config)

    return config

def validate(config):
    settings = {
        "global.metrics.port": int,
        "input.type": str,
        "input.listen.ip": str,
        "input.listen.port": int,
        "input.format": str,
        "metrics": None, # do not basic check for array
    }

    # Basic validation
    for k,v in settings.items():
        c = config

        for p in k.split("."):
            if not p in c:
                raise ConfigError("{} is not specified".format(k))

            if v and type(c[p]) is type(v):
                raise ConfigError("{} have wrong type".format(k))

            c = c[p]

    # Input type
    if config["input"]["type"] != "syslog":
        raise ConfigError("\"{}\" for {} is not supported".format(config["input"]["type"],
                                                                  "input.type"))

    # Predefined formats
    formats = {
        "combined": {
            "format": "regex",
            "regex": '^(?P<remote_addr>[a-f\d:.]+) - (?P<remote_user>[^\s]+) \[(?P<time_local>[^\s]+ [^\s]+)\] "(?P<request_method>[A-Z_]+) (?P<request_uri>[^"]+) HTTP/[^"]+" (?P<status>[\d]+) (?P<body_bytes_sent>[\d]+) "(?P<http_referer>[^"]*)" "(?P<http_user_agent>.*)"$'
        }
    }

    fname = config["input"]["format"]
    if fname in formats:
        # Override data in config
        for k,v in formats[fname].items():
            config["input"][k] = v

    # Check input format support
    fname = config["input"]["format"]
    if not fname in ("regex"):
        raise ConfigError("\"{}\" for {} is not supported".format(fname, "input.format"))

    return config
