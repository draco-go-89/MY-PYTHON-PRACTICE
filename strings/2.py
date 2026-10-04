# This is extremely useful when manipulating text.
message = input("Enter a message: ")

message = message.replace("you", "Python")
print(message)

# Check whether text exists..
if "python" in message or "Python" in message:  # if "Python" in message:
    print("Yes, 'python' is present in the message.")
else:
    print("No, 'python' is not present in the message.")