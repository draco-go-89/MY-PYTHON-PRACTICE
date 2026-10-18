def text_to_binary():
    # Take input from the user
    user_text = input("Enter the text you want to convert to binary: ")
    
    # Convert each character to an 8-bit binary string
    binary_list = [f"{ord(char):08b}" for char in user_text]
    
    # Join the binary blocks with spaces for readability
    binary_output = " ".join(binary_list)
    
    print("\n--- Your 8-Bit Binary Code ---")
    print(binary_output)

# Run the function
if __name__ == "__main__":
    text_to_binary()