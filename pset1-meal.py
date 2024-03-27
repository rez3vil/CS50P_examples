def main():
    query = input("What time is it? ")
    query = float(convert(query))
    if query in float_range(7.00, 8.00, 0.01):
        print("breakfast time")
    elif query in float_range(12.00, 13.00, 0.01):
        print("lunch time")
    elif query in float_range(17.00, 18.00, 0.01):
        print("dinner time")
    else:
        print("else case")

def convert(time):
    if " " in time:
        a, z = time.split()
        x, y = a.split(":")
        if z == "a.m.":
            z = 0
        elif z == "p.m.":
            z = 12
    elif ":" in time:
        x, y = time.split(":")
        z = 0
    x = int(x)
    y = int(y)
    time = x + z + y / 60 
    time = float(time)
    return round(time, 2)

def float_range(i, j, k):
    while i < j:
        yield round(i, 2)
        i += k

if __name__ == "__main__":
    main()
