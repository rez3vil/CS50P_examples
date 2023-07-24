#==================Calculator.py===========================

#basic conditional code using if, elif and else
x = int(input("What's x?"))
y = int(input("What's y?"))
if x < y:
    print ("x is less than y")
elif x > y:
    print ("x is greater than y")
else:
    print ("x is equal to y")

#basic conditional code using if, or and else
x = int(input("What's x?"))
y = int(input("What's y?"))
if x < y or x > y:
    print("x is not equal to y")
else:
    print ("x is equal to y")

#making it more easy and compact
x = int(input("What's x?"))
y = int(input("What's y?"))
if x!=y:
    print("x is not equal to y")
else:
    print ("x is equal to y")
    
#==================Grade.py===========================

#using and as conditional
score = int(input("Score: "))
if score >= 90 and score <= 100:
    print("Grade: A")
elif score >= 80 and score <= 90:
    print("Grade: B")
elif score >= 70 and score <= 80:
    print("Grade: C")
elif score >= 60 and score <= 80:
    print("Grade: D")
else:
    print("Grade: F")

#simplifying above code
score = int(input("Score: "))
if 90 <= score <= 100:
    print("Grade: A")
elif 80 <= score <= 90:
    print("Grade: B")
elif 70 <= score <= 80:
    print("Grade: C")
elif 60 <= score <= 70:
    print("Grade: D")
else:
    print("Grade: F")
