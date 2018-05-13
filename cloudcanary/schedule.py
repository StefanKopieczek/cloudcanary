from collections import namedtuple
from errors import ParseError

DELIMITER = ':'
TimeTrigger = namedtuple('TimeTrigger', ['delay_in_seconds', 'is_recurring'])


def parse_line(line, action_parsers):
    time_part, action_part = line.split(DELIMITER, 1)
    return parse_time(time_part), parse_action(action_part, action_parsers)


def parse_time(time_string):
    time_string = time_string.lower().strip()
    recurrence, time_descriptor = time_string.split(' ', 1)

    is_recurring = None
    if recurrence == 'after':
        is_recurring = False
    elif recurrence == 'every':
        is_recurring = True
    else:
        raise ParseError("I don't understand '{}'; lines should start with 'after' or 'every'".format(time_string))

    if ' ' in time_descriptor:
        # E.g. "after 3 seconds", "every 20 minutes"
        delay, units = time_descriptor.split(' ', 1)
        delay = float(delay)
    else:
        # E.g. "every day"
        delay = 1
        units = time_descriptor

    if units.startswith('sec'):
        pass
    elif units.startswith('min'):
        delay *= 60
    elif units.startswith('hour'):
        delay *= 3600
    elif units.startswith('day'):
        delay *= 3600 * 24
    else:
        raise ParseError("I don't understand '{}'; unknown unit '{}'".format(time_string, units))

    return TimeTrigger(delay, is_recurring)


def parse_action(action_part, action_parsers):
    for parser in action_parsers:
        if parser.canHandle(action_part):
            return parser.parse(action_part)

    raise ParseError("I don't know how to '{}'".format(action_part))
