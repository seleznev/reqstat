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
    # Socket
    if not "socket" in config:
        raise ConfigError("socket is not specified")

    # Worker
    if not "worker" in config or config["worker"] == None:
        raise ConfigError("worker section is not specified or empty")

    if not "threads" in config["worker"]:
        raise ConfigError("worker.threads is not specified")

    # Log
    if not "log" in config or config["log"] == None:
        raise ConfigError("log section is not specified or empty")

    if not "format" in config["log"]:
        raise ConfigError("log.format is not specified")

    if config["log"]["format"] == "combined":
        config["log"]["regex"] = '^(?P<remote_addr>[a-f\d:.]+) - (?P<remote_user>[^\s]+) \[(?P<time_local>[^\s]+ [^\s]+)\] "(?P<request_method>[A-Z_]+) (?P<request_uri>[^"]+) HTTP/[^"]+" (?P<status>[\d]+) (?P<body_bytes_sent>[\d]+) "(?P<http_referer>[^"]*)" "(?P<http_user_agent>.*)"$'
    elif config["log"]["format"] == "json":
        config["log"]["regex"] = None
    elif config["log"]["format"] == "regex":
        if not "regex" in config["log"]:
            raise ConfigError("log.regex is not specified")
    else:
        raise ConfigError("log.format has unsupported value")

    #
    return config
