import json
import collections
from mock import patch
from datetime import datetime
from io import StringIO

from wrapplog import Logger


class TestWrappObserver(object):
    @patch('wrapplog._timestamp')
    def setup(self, timestamp_mock):
        self.timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        timestamp_mock.return_value = self.timestamp
        self.out = StringIO()
        self.msg = 'Hello'
        self.service = "api"
        self.namespace = 'tests'
        self.log = Logger(self.out, service=self.service)

    def _generate_output(self, level):
        res = collections.OrderedDict()
        res['level'] = level
        res['msg'] = self.msg
        res['namespace'] = self.namespace
        res['service'] = self.service
        res['timestamp'] = self.timestamp
        return json.dumps(res) + '\n'

    def test_debug(self):
        self.log.debug(self.msg)
        self.assert_output(self._generate_output('debug'))

    def test_info(self):
        self.log.info(self.msg)
        self.assert_output(self._generate_output('info'))

    def test_warning(self):
        self.log.warning(self.msg)
        self.assert_output(self._generate_output('warning'))

    def test_error(self):
        self.log.error(self.msg)
        self.assert_output(self._generate_output('error'))

    def test_traceback(self):
        try:
            raise ValueError
        except ValueError:
            self.log.error_with_traceback(self.msg)

        actual = json.loads(self.get_output())
        assert actual['level'] == 'error'
        assert actual['trace'] is not None

    def get_output(self):
        self.out.seek(0)
        return self.out.read()

    def assert_output(self, expected):
        actual = self.get_output()
        assert actual == expected, repr(actual)
