
"""
A parser is a python tool that can:

"something that reads command-line arguments"

example: this file is located in parser/example.py

If you run this:
python parser/example.py --name Hamza

You are executing this file, this file captures --name

then prints it

So you get: "Hamza"

"""
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--name")

args = parser.parse_args()

print(args.name)