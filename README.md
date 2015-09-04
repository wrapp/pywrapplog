txwrapplog
==========

Changes to structlog to work according to WEP 007:

* Outputs JSON
* Drop support for critical log level
* `event` key renamed to `msg`
* Add automatic namespace generation for Loggers similar to twisted.logger

```python

In [1]: import wrapplog

In [2]: wrapplog.start_logging()

In [3]: log = wrapplog.Logger()

In [4]: log.info('hello', name='Jane')
INFO {"level": "info", "msg": "hello", "name": "Jane", "namespace": "__main__"}

In [5]: class MyClass(object):
   ...:     log = wrapplog.Logger()
   ...:     def hello(self, name):
   ...:         self.log.warning('HELLO', name=name)
   ...:

In [6]: MyClass().hello('Jane')
WARNING {"level": "warning", "msg": "HELLO", "name": "Jane", "namespace": "__main__.MyClass"}

```

License: MIT
