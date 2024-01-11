#!/usr/bin/env python3
"""
This script obfuscates sensitive information and uses a custom log formatter to redact specific fields.
"""

import os
import logging
import mysql.connector
from re import sub
from typing import List, Tuple


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establish a connection to the database.

    Returns:
        A connection to the database.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passw = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    hosting = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    medb = mysql.connector.connect(
        host=hosting,
        username=username,
        password=passw,
        database=db
    )

    return medb


def get_logger() -> logging.Logger:
    """
    Set up the log formatter.

    Returns:
        A logger with a customized log formatter.
    """
    log: logging.Logger = logging.getLogger('user_data')
    log.propagate = False

    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter((RedactingFormatter(fields=PII_FIELDS)))
    stream_handler.setFormatter(formatter)

    log.addHandler(stream_handler)

    return log


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    """
    Filter and obfuscate sensitive information in the log message.

    Args:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing the obfuscation pattern.
        message: A string representing the log line.
        separator: A string representing the character separating all fields in the log line.

    Returns:
        A string with obfuscated sensitive information.
    """
    for field in fields:
        message = sub(f'{field}=.+?{separator}',
                      f'{field}={redaction}{separator}', message)

    return message


class RedactingFormatter(logging.Formatter):
    """
    Custom log formatter to redact specific fields.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Set the format of the log record.

        Args:
            record: Log record of an event.

        Returns:
            The formatted log record.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)

        return super(RedactingFormatter, self).format(record)


def main():
    """
    Entry point of the script.
    """
    db: mysql.connector.connection.MySQLConnection = get_db()
    cursor = db.cursor()
    headers: Tuple = (head[0] for head in cursor.description)
    cursor.execute("SELECT name, email, phone, ssn, password FROM users;")
    log: logging.Logger = get_logger()

    for row in cursor:
        """
        zip Elements combine two tuples to generate a new tuple.
        """
        data_row: str = ''
        for key, value in zip(headers, row):
            data_row = ''.join(f'{key}={str(value)};')

        log.info(data_row)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
