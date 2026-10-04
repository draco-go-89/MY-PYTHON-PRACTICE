import json #importing Python's built-in JSON module

with open("student.json", "r") as file: #r means read
    student = json.load(file) #It takes the JSON file and converts it into a Python object.

print(student)
print(student["name"])
print(student["skills"])