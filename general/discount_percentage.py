try:
    # Get inputs from the user
    original_price = float(input("Enter the original price (Rs): "))
    discount_percent = float(input("Enter the discount percentage (%): "))

    # Calculate final price
    discount_amount = original_price * (discount_percent / 100)
    final_price = original_price - discount_amount

    # Output the results
    print(f"\n--- Receipt ---")
    print(f"Original Price: Rs {original_price:.2f}")
    print(f"Discount: {discount_percent}% (Rs {discount_amount:.2f})")
    print(f"Final Price: Rs {final_price:.2f}")

except ValueError:
    print("Please enter valid numerical values.")
