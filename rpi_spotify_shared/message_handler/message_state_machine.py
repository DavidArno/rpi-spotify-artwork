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
from enum import Enum
from rpi_spotify_shared.message_handler import message_format

def handle_messages(reader, writer, message_brokers):

    class _States(Enum):
        WaitingForMessageStart = 0,
        HeaderStarted = 1,
        ReadingHeader = 2,
        BodyStarted = 3,
        ReadingBody = 4,
        SkippingToEnd = 5,

    state = _States.WaitingForMessageStart
    header = None
    body = None

    while True:
        char = reader.read()

        if state != _States.ReadingBody and \
           state != _States.SkippingToEnd and \
           char == message_format.MESSAGE_BODY_END:
            writer.write(message_format.UNEXPECTED_MESSAGE_END)
            state = _States.WaitingForMessageStart
        else:
            match state:
                case _States.WaitingForMessageStart:
                    if (char == message_format.MESSAGE_START):
                        state = _States.HeaderStarted

                case _States.HeaderStarted:
                    if char == message_format.MESSAGE_BODY_START:
                        writer.write(message_format.MISSING_HEADER)
                        state = _States.SkippingToEnd
                    else:
                        header = char
                        state = _States.ReadingHeader

                case _States.ReadingHeader:
                    if char == message_format.MESSAGE_BODY_START:
                        state = _States.BodyStarted
                    else:
                        header += char

                case _States.BodyStarted:
                    body = char
                    state = _States.ReadingBody

                case _States.ReadingBody:
                    if char == message_format.MESSAGE_BODY_END:
                        if header in message_brokers:
                            result = message_format.SUCCESS if message_brokers[header](body) else message_format.FAILURE
                        else:
                            result = message_format.UNKNOWN_HEADER

                        writer.write(result)
                        state = _States.WaitingForMessageStart
                    else:
                        body += char

                case _States.SkippingToEnd:
                    if char == message_format.MESSAGE_BODY_END:
                        state = _States.WaitingForMessageStart
