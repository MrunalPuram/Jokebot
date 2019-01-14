import time
import csv
import sys

def deliver(prompt, punchline):
    print(prompt)
    time.sleep(2)
    print(punchline)

# deliver("Hello", "World")

def read_input():
    user_input = input("'next' or 'quit'?\n")
    if user_input == "next":
        return True
    elif user_input == "quit":
        return False
    else:
        print("I don't understand, please input 'next' or 'quit'")
        return read_input()


# read_input()

def read_joke(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        joke_list = list(reader)
    return joke_list

read_joke("jokes.csv")

def main():
    if (len(sys.argv) < 2):
        print("No joke file given")
        exit()
    file_name = sys.argv[1]
    jokes_list = read_joke(file_name)
    for joke in jokes_list:
        deliver(joke[0], joke[1])
        if not read_input():
            exit()
    print("We're out of jokes!")
    exit()

if __name__ == '__main__':
    main()