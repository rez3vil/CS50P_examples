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
