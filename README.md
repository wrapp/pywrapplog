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

License: MIT
