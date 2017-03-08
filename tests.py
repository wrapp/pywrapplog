import json
import collections
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
        self.msg = 'Hello'
        self.service = "api"
        self.host = "host-01"
        self.namespace = 'tests'
        self.metric_value = 10
        self.event_data = {"user": {"name": "jude", "id": 1}}
        self.log = Logger(self.out, service=self.service, host=self.host)

    def _generate_output(self, level):
        ''' Outputs the fields in an ordered way as per test expectations
        Order is the following:
        - level
        - msg (For all log levels apart from 'metric' and 'event')
        - event (Applicable for 'event' level)
        - metric (Applicable for 'metric' level)
        - all other fields are ordered in alphabetical order
        - namespace is not applicable to 'event' and 'metric' level
        '''
        def generate_event_output():
            res = collections.OrderedDict()
            res['level'] = level
            res['event'] = self.msg
            res['data'] = self.event_data
            res['host'] = self.host
            res['service'] = self.service
            res['timestamp'] = self.timestamp
            return res

        def generate_metric_output():
            res = collections.OrderedDict()
            res['level'] = level
            res['metric'] = self.msg
            res['host'] = self.host
            res['service'] = self.service
            res['timestamp'] = self.timestamp
            res['value'] = self.metric_value
            return res

        def generate_default_output():
            ''' Applies to all other log levels apart from event and metric '''
            res = collections.OrderedDict()
            res['level'] = level
            res['msg'] = self.msg
            res['host'] = self.host
            res['namespace'] = self.namespace
            res['service'] = self.service
            res['timestamp'] = self.timestamp
            return res

        output_dict = {}
        if level == 'event':
            output_dict = generate_event_output()
        elif level == 'metric':
            output_dict = generate_metric_output()
        else:
            output_dict = generate_default_output()
        return '%s %s\n' % (level.upper(), json.dumps(output_dict))

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

    def test_event(self):
        self.log.event(self.msg, self.event_data)
        self.assert_output(self._generate_output('event'))

    def test_metric(self):
        self.log.metric(self.msg, self.metric_value)
        self.assert_output(self._generate_output('metric'))

    def get_output(self):
        self.out.seek(0)
        return self.out.read()

    def assert_output(self, expected):
        actual = self.get_output()
        assert actual == expected, repr(actual)
