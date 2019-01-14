import time
import csv
import sys
import requests
import json

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

def read_reddit():
    r = requests.get('https://www.reddit.com/r/dadjokes.json', headers={'User-agent': 'jokebot'})
    jokes = r.json()
    clean_jokes = []
    json_data = json.loads(r.text)
    # print(json_data)
    # print(jokes)
    question_list = ["Why", "What", "How"]
    for joke in json_data["data"]["children"]:
        if not joke["data"]["over_18"] and joke["data"]["selftext"]:
            first_word = joke["data"]["title"].split(' ')[0]
            if first_word in question_list:
                clean_jokes.append([joke["data"]["title"], joke["data"]["selftext"]])
    return clean_jokes

# read_reddit()

def main():
    if (len(sys.argv) > 1):
        file_name = sys.argv[1]
        jokes_list = read_joke(file_name)
    else:
        jokes_list = read_reddit()
    for joke in jokes_list:
        deliver(joke[0], joke[1])
        if not read_input():
            exit()
    print("We're out of jokes!")
    exit()

if __name__ == '__main__':
    main()