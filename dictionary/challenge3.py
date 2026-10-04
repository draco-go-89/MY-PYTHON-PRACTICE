def cal_total(numbers):
    total = 0

    for number in numbers:
        total = total + number

    return total

result = cal_total([10, 20, 30, 40])

print(result)