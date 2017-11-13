import arrow


def days_ago(dt_string):
    return (arrow.utcnow() - arrow.get(dt_string)).days
