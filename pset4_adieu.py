import inflect

def main():
    p = inflect.engine()
    empty_set = []
    while True:
        try:
            user = input("Name: ").capitalize()
            empty_set.append(user)
        except EOFError:
            break
    print("\nAdieu, adieu, to " + p.join(empty_set))

if __name__ == "__main__":
    main()
