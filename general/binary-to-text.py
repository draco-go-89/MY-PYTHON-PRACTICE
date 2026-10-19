def binary_to_text(binary_string):
    # Remove any spaces from the input string
    clean_binary = binary_string.replace(" ", "")
    
    # Split the string into chunks of 8 bits (1 byte)
    bytes_list = [clean_binary[i:i+8] for i in range(0, len(clean_binary), 8)]
    
    try:
        # Convert each 8-bit block into a character and join them together
        text = "".join([chr(int(b, 2)) for b in bytes_list])
        return text
    except ValueError:
        return "Error: Invalid binary format. Please use only 0s and 1s."

# Get dynamic input from the user
user_input = input("Enter your binary sequence (separated by spaces or combined): ")
decoded_text = binary_to_text(user_input)

print(f"\nDecoded Text: {decoded_text}")
