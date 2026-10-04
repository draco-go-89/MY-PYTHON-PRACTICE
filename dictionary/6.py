def avg(marks):
    total=0

    for mark in marks:
        total = total + mark

    average = total / len(marks) #len()
    return average

marks = [80, 75, 90, 65, 85] 

result = avg(marks)  #calculation

print("Average: ", result) #return

# 🔥 This is actual programming. WTF!