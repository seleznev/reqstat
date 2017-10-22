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
    return config

def validate(config):
    try:
        main_validate(config)
        return config
    except ConfigError as e:
        raise ConfigError(e.message)
        return None

def main_validate(config):
    pass # TODO

