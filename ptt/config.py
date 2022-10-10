import os
import sys
import logging
import yaml
from collections import UserDict

log = logging.getLogger(__name__)


class Config(UserDict):
    def load(self, config_path):
        """
        Loads configuration from yaml file.
        """
        try:
            with open(os.path.expanduser(config_path), 'r') as f:
                try:
                    self.data = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    log.error(
                        'Error parsing yaml of configuration file '
                        '{}: {}'.format(
                            e.problem_mark,
                            e.problem,
                        )
                    )
                    sys.exit(1)
        except FileNotFoundError:
            log.error(
                'Error opening configuration file {}'.format(config_path)
            )
            sys.exit(1)

    def get(self, key):
        """
        Fetch the configuration value of the specified key. If there are nested
        dictionaries, a dot notation can be used.

        So if the configuration contents are:

        self.data = {
            'first': {
                'second': 'value'
            },
        }

        self.data.get('first.second') == 'value'

        Arguments:
            key(str): Configuration key to fetch
        """
        keys = key.split('.')
        value = self.data.copy()

        for key in keys:
            value = value[key]

        return value
