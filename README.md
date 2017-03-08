wrapplog
========

Changes to structlog to work according to WEP 007:

* Outputs JSON
* Drop support for critical log level
* Add automatic namespace generation for Loggers similar to twisted.logger

```python

In [1]: import wrapplog

In [2]: log = wrapplog.Logger()

In [3]: log.info('hello', name='Jane')
INFO {"level": "info", "msg": "hello", "name": "Jane", "service": None, "host":None, "namespace": "__main__"}

In [4]: class MyClass(object):
   ...:     log = wrapplog.Logger()
   ...:     def hello(self, name):
   ...:         self.log.warning('HELLO', name=name)
   ...:

In [5]: MyClass().hello('Jane')
WARNING {"level": "warning", "msg": "HELLO", "name": "Jane", "service": None, "host":None, "namespace": "__main__.MyClass"}

```

Logging event data
==================

**EVENT:**
A level similar to `info`, but with a consistent *format* for a specific *behavior*, i.e. to log events apart from arbitrary information. This format would be of the following form where event data would be included in the `data` field:

```json
EVENT {"level": "event", "event": "user_created", "data": {"user": {"name": "jude", "id": 1}}, "host": "host-01", "namespace": "tests", "service": "api", "timestamp": "2017-03-08T12:34:59Z"}
```

```python

In [1]: import wrapplog
In [2]: log = wrapplog.Logger()
In [3]: log.event('user_created', {"user": {"name": "jude", "id": 1}})
```

**METRIC:**
For things you need to measure, you can log those instruments with a number value.

```json
METRIC {"level": "metric", "metric": "offers.deployed", "host": "host-01", "namespace": "tests", "service": "api", "timestamp": "2017-03-08T12:34:59Z", "value": 1}
```

```python

In [1]: import wrapplog
In [2]: log = wrapplog.Logger()
In [3]: log.metric('offers.deployed', value=1)
```


License: MIT
