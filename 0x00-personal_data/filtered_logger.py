#!/usr/bin/env python3
"""Using Regex: Write a function called filter_datum that returns
the log message obfuscated:

Arguments:
fields: a list of strings representing all fields to obfuscate

redaction: a string representing by what the field will be obfuscated

message: a string representing the log line

separator: a string representing by which character is separating all
fields in the log line (message) The function should use a regex to
replace occurrences of certain field values.

filter_datum should be less than 5 lines long and use re.sub to
perform the substitution with a single regex
"""

from typing import Sequence, Tuple
import re
import logging


def filter_datum(fields: Sequence[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfucate data by the given field"""
    for field in fields:
        message = re.sub(fr'{field}=(?:.+?){separator}',
                         f'{field}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """obfuscate and format record before logging"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record),self.SEPARATOR)
