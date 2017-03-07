from mock import patch
from datetime import datetime
from cStringIO import StringIO

from wrapplog import Logger


class TestWrappObserver(object):
    @patch('wrapplog._timestamp')
    def setup(self, timestamp_mock):
        self.timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        timestamp_mock.return_value = self.timestamp
        self.out = StringIO()
        self.log = Logger(self.out)

    def test_debug(self):
        self.log.debug('Hello!')
        self.assert_output('DEBUG {"level": "debug", "msg": "Hello!", "namespace": "tests", "timestamp": "%s"}\n' % self.timestamp)

    def test_info(self):
        self.log.info('Hello!')
        self.assert_output('INFO {"level": "info", "msg": "Hello!", "namespace": "tests", "timestamp": "%s"}\n' % self.timestamp)

    def test_warning(self):
        self.log.warning('Hello!')
        self.assert_output('WARNING {"level": "warning", "msg": "Hello!", "namespace": "tests", "timestamp": "%s"}\n' % self.timestamp)

    def test_error(self):
        self.log.error('Hello!')
        self.assert_output('ERROR {"level": "error", "msg": "Hello!", "namespace": "tests", "timestamp": "%s"}\n' % self.timestamp)

    def get_output(self):
        self.out.seek(0)
        return self.out.read()

    def assert_output(self, expected):
        actual = self.get_output()
        assert actual == expected, repr(actual)
