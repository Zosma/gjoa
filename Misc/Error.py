import sys


def error(msg="Something went wrong!"):
    msg = "Error: " + msg
    print(msg)
    sys.exit()