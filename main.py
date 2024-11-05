



def main():
    token = "UNKNOWN_TOKEN"
    with open("token.txt") as file:
        for line in file:
            token = line
    print("SUCCESS")

if __name__ == '__main__':
    main()
