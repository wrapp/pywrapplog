wrapplog
========

Changes to structlog to work according to WEP 007:

* Outputs JSON
* Drop support for critical log level
* Add automatic namespace generation for Loggers similar to twisted.logger

Note that, according to WEP 007, the *service* is a mandatory field in the JSON log entries.
This can be set either while initializing the logger or picked up automatically from a *SERVICE_NAME* environment variable.

```python

In [1]: import wrapplog

In [2]: log = wrapplog.Logger(service="api")

In [3]: log.info('hello', name='Jane')
INFO {"level": "info", "msg": "hello", "service":"api", "name": "Jane", "namespace": "__main__"}

In [4]: class MyClass(object):
   ...:     log = wrapplog.Logger(service="api")
   ...:     def hello(self, name):
   ...:         self.log.warning('HELLO', name=name)
   ...:

In [5]: MyClass().hello('Jane')
WARNING {"level": "warning", "msg": "HELLO", "name": "Jane", "service": "api", "namespace": "__main__.MyClass"}

```

License: MIT
