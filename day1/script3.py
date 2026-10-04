students = [
    {"name": "Lubo Labao", "age": 20, "college": "XYZ University"},
    {"name": "Dhrubo Basumatary", "age": 22, "college": "ABC College"},
    {"name": "Ansula Daimari", "age": 21, "college": "PQR Institute"}
]   

for student in students:
    print("My name is " + student["name"] + " and I am " + str(student["age"]) + " years old and I study in " + student["college"])