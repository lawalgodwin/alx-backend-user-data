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

from typing import List
import re
import logging
import mysql.connector
from os import getenv
# import MySQLdb (this works but mysql.connecor did not work)

PII_FIELDS = ("ssn", "password", "email", "phone", "name")


def filter_datum(fields: List[str], redaction: str, message: str,
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

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """obfuscate and format record before logging"""
        message = filter_datum(self.fields, self.REDACTION,
                               super(RedactingFormatter, self).format(record),
                               self.SEPARATOR)
        return message


def get_logger() -> logging.Logger:
    """Return a logger object"""
    user_data_logger = logging.getLogger("user_data")
    user_data_logger.propagate = False
    loger_handler = logging.StreamHandler()
    formater = RedactingFormatter(list(PII_FIELDS))
    loger_handler.setFormatter(formater)
    user_data_logger.setLevel(logging.INFO)
    user_data_logger.addHandler(loger_handler)
    return user_data_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the mysql database
    NB: pip3 install mysql-connector-python
    """
    DB_HOST = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    DB_NAME = getenv("PERSONAL_DATA_DB_NAME")
    DB_USER = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    DB_PASSWORD = getenv("PERSONAL_DATA_DB_PASSWORD", "")

    try:
        database_connector = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME)
        return database_connector
    except Exception as e:
        print(F"Error: ", e)
        return e
