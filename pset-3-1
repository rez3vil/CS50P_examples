def main():
    while True:
        try:
            user = input("Fraction: ")
            x, y = map(int, user.split("/"))
            if x > y or y == 0:
                continue
            z = round((x/y)*100)
            if z <= 1:
                return "E"
            elif z >= 99:
                return "F"
            else:
                return f"{z}%"
        except (ValueError, ZeroDivisionError):
            pass

print(main())
