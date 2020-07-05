import base64
import os
from configparser import ConfigParser


class Config:
    def __init__(self):
        self._file_path = f'{os.path.dirname(__file__)}/conf.ini'
        self._parser = ConfigParser()
        self._parser.read(self._file_path)

    def get_email_config(self, section='email'):
        email = {}
        if self._parser.has_section(section):
            params = self._parser.items(section)
            for param in params:
                email[param[0]] = param[1]
        email['password'] = base64.b64decode(email['password']).decode('utf-8')

        return email

    def get_params_config(self, section='monit_params'):
        monit_params = {}
        if self._parser.has_section(section):
            params = self._parser.items(section)
            for param in params:
                monit_params[param[0]] = param[1]

        return monit_params

    def get_periodics_config(self, section='periodics'):
        periodics = {}
        if self._parser.has_section(section):
            params = self._parser.items(section)
            for param in params:
                periodics[param[0]] = param[1]

        return periodics
