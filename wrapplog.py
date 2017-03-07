import os
import json
import inspect
import collections

import structlog
from structlog.processors import JSONRenderer
from structlog import PrintLogger, wrap_logger, PrintLoggerFactory


# Deprecated
def start_logging(output=None):
    structlog.configure(
            logger_factory=structlog.PrintLoggerFactory(output),
            processors=[render_wrapp_log])


class Logger(object):
    def __init__(self, output=None, namespace=None, source=None):
        log = wrap_logger(
                        PrintLogger(output),
                        processors=[
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


def order_fields(_, level, event_dict):
    res = collections.OrderedDict()
    res['level'] = level
    res['msg'] = event_dict.pop('event')
    res.update(sorted(event_dict.items()))
    return res

def render_wrapp_log(_, level, event_dict):
    return level.upper() + ' ' + event_dict
