from cStringIO import StringIO
from wrapplog import Logger, start_logging



class TestWrappObserver(object):
    def setup(self):
        self.out = StringIO()
        start_logging(self.out)
        self.log = Logger()

    def test_debug(self):
        self.log.debug('Hello!')
        self.assert_output('DEBUG {"level": "debug", "msg": "Hello!", "namespace": "tests"}\n')

    def test_info(self):
        self.log.info('Hello!')
        self.assert_output('INFO {"level": "info", "msg": "Hello!", "namespace": "tests"}\n')

    def test_warning(self):
        self.log.warning('Hello!')
        self.assert_output('WARNING {"level": "warning", "msg": "Hello!", "namespace": "tests"}\n')

    def test_error(self):
        self.log.error('Hello!')
        self.assert_output('ERROR {"level": "error", "msg": "Hello!", "namespace": "tests"}\n')

    def get_output(self):
        self.out.reset()
        return self.out.read()

    def assert_output(self, expected):
        actual = self.get_output()
        assert actual == expected, repr(actual)
