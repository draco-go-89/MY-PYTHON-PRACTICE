def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # Return the index if found
    return -1  # Return -1 if the target is not in the list

# Define a sample array (list)
my_array = [23, 8, 42, 4, 16, 15]

# --- Test Case 1: Searching for a number that exists ---
target_1 = 4
result_1 = linear_search(my_array, target_1)
print(f"Searching for {target_1}...")
print(f"Target found at index: {result_1}\n")  # Expected Output: 3

# --- Test Case 2: Searching for a number that DOES NOT exist ---
target_2 = 99
result_2 = linear_search(my_array, target_2)
print(f"Searching for {target_2}...")
print(f"Target found at index: {result_2}")    # Expected Output: -1
