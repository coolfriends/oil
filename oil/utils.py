import arrow

VERSION = '0.0.1'


def days_ago(dt_string):
    return (arrow.utcnow() - arrow.get(dt_string)).days


def version():
    return VERSION
