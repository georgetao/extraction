"""
This script is for unpacking relevant information from 
the EPA dataset which is a json file 
"""

# imports
import sys

for line in sys.stdin:
    content = line.split()
    print(content)
