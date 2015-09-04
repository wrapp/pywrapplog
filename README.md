txwrapplog
==========

Changes to structlog to work according to WEP 007:

* Outputs JSON
* Drop support for critical log level
* `event` key renamed to `msg`
* Add automatic namespace generation for Loggers similar to twisted.logger

License: MIT
