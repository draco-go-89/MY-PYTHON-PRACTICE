student = {
    "name": "Dhrubo",
    "age": 20,
    "course": "B.TECH CSE"
}
# can also use pop() student.pop("age")
student["age"] = 21  #Changing a value
student["city"] = "Delhi" #Adding a new value

print(student["name"])
print(student["age"])
print(student["course"])

print(student["city"])  #this code was written after addning a new value city

# for pop()
# student = {
#     "name": "Dhrubo",
#     "age": 20,
#     "city": "Delhi"
# }

# student.pop("city")

# print(student)