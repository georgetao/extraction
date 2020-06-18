#!/usr/bin/python3

def test(task):
	x = len(task)
	print('Length of Item 1: ' + str(x))
	return 'Length of Item 1: ' + str(x)

file = open("temp.txt", "r")
message = file.read()

test(message)