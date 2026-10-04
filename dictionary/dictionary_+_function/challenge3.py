# Create a list containing 3 students, where every student is a dictionary
# Here we use a for loop to print the output

students = [
    {"name": "Dhrubo", "marks": 85},
    {"name": "Daimari", "marks": 72},
    {"name": "Alien", "marks": 91}
]

for student in students: # This takes each dictionary one at a time.
    print(student["name"], "-", student["marks"])


# BONUS PROGRAM 
h_student = students[0] #We start by assuming the first student has the highest marks

for student in students:
    if student["marks"] > h_student["marks"]: # Then the loop checks each students highest marks >
        h_student = student # then it results out the highest marks and student

print() #this print() creates space with another print above
print("Highest marks:", h_student["name"])
print("Marks:", h_student["marks"])

# List
#  ↓
# Dictionary
#  ↓
# Loop
#  ↓
# Condition
#  ↓
# Compare values
#  ↓
# Find result