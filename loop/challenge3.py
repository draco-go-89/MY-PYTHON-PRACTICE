secret = "python123"

while True:
    guess = input("Enter password: ")

    if guess == secret:
        print("Login successful!")
        break
    else:
        print("Wrong password!")


