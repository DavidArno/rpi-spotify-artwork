################################################################################
# 
# handle_message(reader, writer, message_brokers)
# - reader must be an object that provides a read() function that returns a
#   single character in a string
# - write must be an object that provides a write(str) function
# - message_brokers must be a dictionary of form: message_name : handler
#   where message_name is a string and handler is a func(message_body : str)
#   function.
# 
# The messages sent very reader.read() must be of the form as EBNF:
# 
# message = message_start , message_header , body_start , body , message_end ;
# message_start = '@' ;
# message_header = allowed_char , { allowed_char } ;
# body_start = ':' ;
# body = allowed_char, { allowed_char } ;
# message_end = ';' ;
# allowed_char = letter | digit | allowed_symbol ;
# letter = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | 
#          "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | 
#          "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | 
#          "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | 
#          "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" ;
# digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
# allowed_symbol = '!' | '"' | '#' | '$' | '$' | '%' | '^' | '&' | '*' | '(' |
#                  ')' | '_' | '-' | '+' | '=' | '{' | '}' | '[' | ']' | "'" |
#                  '#' | '~' | '<' | '>' | ',' | '.' | '|' | '?' | '/' | '\' ;
# 
# So the message must be @head:body; where head and body must be at least one
# character each.
# ############################################################################## 
import compatibility

if compatibility.running_as_cpython:
    from enum import Enum
    from typing import Callable
    Reader = Callable[[], str]
    Writer = Callable[[str], None]
else:
    Enum = object # type: ignore
    Reader = callable # type: ignore
    Writer = callable # type: ignore

from rpi_spotify_shared.message_handler import message_format
from rpi_spotify_shared.message_handler.message_types import MessageBrokers, MessageHeader, MessageBody

def handle_messages(read:Reader, write:Writer, message_brokers:MessageBrokers):

    class _States(Enum):
        WaitingForMessageStart = 0,
        HeaderStarted = 1,
        ReadingHeader = 2,
        BodyStarted = 3,
        ReadingBody = 4,
        SkippingToEnd = 5,

    state = _States.WaitingForMessageStart
    header = ""
    body = ""

    while True:
        char = read()

        if state != _States.ReadingBody and \
           state != _States.SkippingToEnd and \
           char == message_format.MESSAGE_BODY_END:
            write(message_format.UNEXPECTED_MESSAGE_END)
            state = _States.WaitingForMessageStart

        elif state == _States.WaitingForMessageStart:
            if (char == message_format.MESSAGE_START):
                state = _States.HeaderStarted

        elif state == _States.HeaderStarted:
            if char == message_format.MESSAGE_BODY_START:
                write(message_format.MISSING_HEADER)
                state = _States.SkippingToEnd
            else:
                header = char
                state = _States.ReadingHeader

        elif state == _States.ReadingHeader:
            if char == message_format.MESSAGE_BODY_START:
                state = _States.BodyStarted
            else:
                header += char

        elif state == _States.BodyStarted:
            body = char
            state = _States.ReadingBody

        elif state == _States.ReadingBody:
            if char == message_format.MESSAGE_BODY_END:
                if header in message_brokers:
                    result = message_format.SUCCESS \
                        if message_brokers[MessageHeader(header)](MessageBody(body)) \
                        else message_format.FAILURE
                else:
                    result = message_format.UNKNOWN_HEADER

                write(result)
                state = _States.WaitingForMessageStart
            else:
                body += char

        else:
            if char == message_format.MESSAGE_BODY_END:
                state = _States.WaitingForMessageStart
