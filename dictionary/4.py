student = {
    "name": "Dhrubo",
    "age": 20,
    "course": "B.Tech CSE"
}

print(student.keys())

for key in student:  #Getting all keys
    print(key)

for value in student.values():  #Getting all values
    print(value)

for key, value in student.items(): #Getting both key AND value. This is very important. Use .items()
    print(key, ":", value) #example: 'key' is name and 'value' is dhrubo
