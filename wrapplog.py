import os
import json
import inspect
import collections
from datetime import datetime

import structlog
from structlog.processors import JSONRenderer
from structlog import wrap_logger, BoundLogger, PrintLogger, PrintLoggerFactory


# Deprecated
def start_logging(output=None):
    return


class NumberValueError(Exception):
    pass


class WrappPrintLogger(PrintLogger):
    def msg(self, message):
        return super(WrappPrintLogger, self).msg(message)

    event = metric = msg


class WrappLogger(BoundLogger):
    def event(self, name, data=None):
        return super(WrappLogger, self)._proxy_to_logger('event', name, data=data)

    def metric(self, name, value=1):
        try:
            float(value)
        except ValueError:
            raise NumberValueError(value)
        return super(WrappLogger, self)._proxy_to_logger('metric', name, value=value)


class Logger(object):
    def __init__(self, output=None,
                 namespace=None, source=None,
                 service=None, host=None):
        log = wrap_logger(
                        WrappPrintLogger(output),
                        wrapper_class=WrappLogger,
                        processors=[
                            add_timestamp,
                            order_fields,
                            JSONRenderer(),
                            render_wrapp_log,
                        ])

        if not namespace:
            try:
                frame = inspect.currentframe(1)
                namespace = frame.f_globals['__name__']
            except:
                namespace = 'unknown'
        self._log = log.bind(namespace=namespace)

        service = service or os.environ.get('SERVICE_NAME')
        self._log = self._log.bind(service=service)

        host = host or os.environ.get('HOSTNAME')
        self._log = self._log.bind(host=host)

    def __get__(self, oself, type=None):
        if oself is None:
            source = type
        else:
            source = oself

        return self.__class__(
            ".".join([type.__module__, type.__name__]),
            source,
        )

    def debug(self, *args, **kwargs):
        return self._log.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self._log.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self._log.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self._log.error(*args, **kwargs)

    def event(self, name, data=None):
        """Logs an event.

        :param name: Name of the event
        :param data: Dictionary holding data to describe the event
        """
        data = data or {}
        return self._log.event(name, data=data)

    def metric(self, name, value=1):
        """Logs a metric.

        :param name: Name of the metric
        :param value: A number holding the value of the metric
        """
        return self._log.metric(name, value=value)


def _timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def add_timestamp(_, __, event_dict):
    event_dict['timestamp'] = _timestamp()
    return event_dict


def order_fields(_, level, event_dict):
    res = collections.OrderedDict()
    res['level'] = level
    # Levels 'event' and 'metric', don't require 'namespace' and 'msg' fields.
    # Instead, they would require the fields 'event' and 'metric'
    # respectively for the name of the event and metric.
    if level in ["event", "metric"]:
        event_dict.pop('namespace')
        key = level
    else:
        key = "msg"
    res[key] = event_dict.pop('event')
    res.update(sorted(event_dict.items()))
    return res


def render_wrapp_log(_, level, event_str):
    return level.upper() + ' ' + event_str
