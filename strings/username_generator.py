first_name = input("Enter first name: ")
last_name = input("Enter last name: ")

first_name = first_name.strip().lower()
last_name = last_name.strip().lower()

username = first_name + "_" + last_name

print(f"Your username is: {username}")
