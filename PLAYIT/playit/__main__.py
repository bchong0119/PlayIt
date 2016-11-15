#!/usr/bin/env python

import tornado.options

from playit.web import Application

if __name__ == '__main__':
    tornado.options.parse_command_line()

    application = Application()
    application.run()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
