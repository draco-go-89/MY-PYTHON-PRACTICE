age = int(input("Enter your age: "))
have_ticket = True

if age >= 18:
    if have_ticket:
        print("You can enter the concert")
else:
    print("You need a ticket to enter the concert")
