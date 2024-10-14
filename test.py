import os
import sys

# Unused import
import math


def example_function(x):
    if x > 10:  # This should have a docstring
        print("Greater than 10")
    else:
        print("10 or less")

# Function with too many local variables


def complex_function(a, b, c, d, e, f, g):
    result1 = a + b
    result2 = c + d
    result3 = e + f
    result4 = g + a
    return result1, result2, result3, result4

# Function with no return statement


def no_return_statement():
    print("This function does not return anything")

# Long line exceeding 79 characters


def long_line():
    print("This is a very long line that exceeds the maximum recommended line length of 79 characters.")

# Function vulnerable to command injection (security issue)


def insecure_function(command):
    os.system(command)

# Using main to execute the script


if __name__ == "__main__":
    # Unused variable
    unused_var = 42
    example_function(15)
    long_line()
