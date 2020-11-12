#! /usr/bin/env python3


def brokenFunction():
    a = 0
    return 2 / a

if __name__ == "__main__":
    print("Calling brokenFunction")
    c = brokenFunction()
