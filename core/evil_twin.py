import random as rd
import scapy
import sys
import os

file = os.path.join("evil_twin.sh")


with open(file as "r"):
    code = file.read()
    exec(code)
        