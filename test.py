import csv


with open("pieces.csv", "r") as pieces:
    test = pieces.readline()
    print(test.strip())