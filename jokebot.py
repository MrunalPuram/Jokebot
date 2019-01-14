import time
import csv
import sys
import requests
import json

# Prints prompt, waits 2 seconds, prints punchline
def deliver(prompt, punchline):
    print(prompt)
    time.sleep(2)
    print(punchline)

# Reads user input on whether to proceed or exit
def read_input():
    user_input = input("--- 'next' or 'quit'? ---\n--> ")
    if user_input == "next":
        return True
    elif user_input == "quit":
        return False
    else:
        print("--- I don't understand, please input 'next' or 'quit' ---")
        return read_input()

# Reads CSV file and compiles list of jokes
def read_csv(file_name):
    try:
        f = open(file_name, 'r')
    except IOError:
        print("--- Could not read file, fetching jokes from Reddit ---")
        return read_reddit()
    with f:
        reader = csv.reader(f)
        # joke_list = list(reader)
        joke_list = []
        for row in reader:
            # Check if row has exactly 2 entries
            if len(row) == 2:
                joke_list.append(row)
    return joke_list

# Compiles jokes from Reddit posts on /r/dadjokes
def read_reddit():
    r = requests.get('https://www.reddit.com/r/dadjokes.json', headers={'User-agent': 'jokebot'})
    clean_jokes = []
    json_data = json.loads(r.text)
    question_list = ["Why", "What", "How"]

    # Filter json data and collect joke title and body
    for joke in json_data["data"]["children"]:
        if not joke["data"]["over_18"] and joke["data"]["selftext"]:
            first_word = joke["data"]["title"].split(' ')[0]
            if first_word in question_list:
                clean_jokes.append([joke["data"]["title"], joke["data"]["selftext"]])
    return clean_jokes


def main():
    if (len(sys.argv) > 1):
        file_name = sys.argv[1]
        jokes_list = read_csv(file_name)
    else:
        jokes_list = read_reddit()
    for joke in jokes_list:
        deliver(joke[0], joke[1])
        if not read_input():
            exit()
    print("--- We're out of jokes! ---")
    exit()

if __name__ == '__main__':
    main()