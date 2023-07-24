#using return values to get the return of the value in defined function
def main():
    x = int(input("What's x?"))
    print("x squared is", square(x))

def square(n):
    return n*n

main()
