import collections
import inspect
import json
import structlog



def start_logging(output=None):
    structlog.configure(
            logger_factory=structlog.PrintLoggerFactory(output),
            processors=[render_wrapp_log])


class Logger(object):
    def __init__(self, namespace=None, source=None):
        if not namespace:
            try:
                frame = inspect.currentframe(1)
                namespace = frame.f_globals['__name__']
            except:
                namespace = 'unknown'
        self._log = structlog.get_logger(namespace=namespace)

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



def render_wrapp_log(logger, method_name, event_dict):
    res = collections.OrderedDict()
    level = method_name

    res['level'] = method_name
    res['msg'] = event_dict.pop('event')
    res.update(sorted(event_dict.items()))
    data = json.dumps(res, cls=structlog.processors._JSONFallbackEncoder)
    return level.upper() + ' ' +  data
