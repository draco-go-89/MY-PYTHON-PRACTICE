rows = 40

for i in range (1, rows + 1):
    for j in range(rows, rows - i, -1):
        print(j, end=" ")
    print()