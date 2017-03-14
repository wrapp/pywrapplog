import os
import json
import inspect
import collections
from datetime import datetime

import structlog
from structlog.processors import JSONRenderer
from structlog import wrap_logger, PrintLogger, PrintLoggerFactory


# Deprecated
def start_logging(output=None):
    return


class Logger(object):
    def __init__(self, output=None,
                 namespace=None, source=None, service=None):
        log = wrap_logger(
                        PrintLogger(output),
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

        self._log = log.bind(namespace=namespace, service=service)

    def debug(self, *args, **kwargs):
        return self._log.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self._log.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self._log.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self._log.error(*args, **kwargs)


def _timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def add_timestamp(_, __, event_dict):
    event_dict['timestamp'] = _timestamp()
    return event_dict


def order_fields(_, level, event_dict):
    res = collections.OrderedDict()
    res['level'] = level
    res["msg"] = event_dict.pop('event')
    res.update(sorted(event_dict.items()))
    return res


def render_wrapp_log(_, level, event_str):
    return level.upper() + ' ' + event_str
