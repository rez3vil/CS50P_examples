#using return values to get the return of the value in defined function
def main():
    x = int(input("What's x?"))
    print("x squared is", square(x))

def square(n):
    return n*n
    #you can use return n ** 2 / return pow (n, 2) as well instead of n*n

main()
