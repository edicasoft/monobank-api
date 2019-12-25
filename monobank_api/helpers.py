import time


def to_timestamp(dtime):
    """Converts datetime to unix timestamp"""
    return int(time.mktime(dtime.timetuple()))
