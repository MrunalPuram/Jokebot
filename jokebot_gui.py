from tkinter import *
from tkinter import ttk

import time
import csv
import sys
import requests
import json


# Prints prompt, waits 2 seconds, prints punchline
def deliver(prompt, punchline):
    prompt_string.set(prompt)
    next_button.pack_forget()
    root.update()
    time.sleep(2)
    punch_string.set(punchline)
    next_button.pack()
    root.update()

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


# Global variables
jokes_list = []
joke_iter = iter(jokes_list)


def main():
    global jokes_list
    global joke_iter
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        jokes_list = read_csv(file_name)
    else:
        jokes_list = read_reddit()
    joke_iter = iter(jokes_list)
    next_question()  # Call to display first joke


# Function for next button
def next_question():
    prompt_string.set("")
    punch_string.set("")
    try:
        joke = next(joke_iter)
        deliver(joke[0], joke[1])
    except StopIteration:
        prompt_string.set("We're out of jokes!")
        prompt_label.update()
        time.sleep(5)
        exit()


# GUI
# Root Window setup
root = Tk()
root.title("JokeBot")
root.geometry("500x500")  # Fixme Hardcoded window size

# Title Label
display_string = StringVar()
display = ttk.Label(root, textvariable=display_string, font=("Courier", 40))
# display.place(x=200, y=10)
display.pack()
display_string.set("JokeBot")

# Prompt Label
prompt_string = StringVar()
prompt_label = ttk.Label(root, textvariable=prompt_string, font=("Courier", 20), wraplength=480)
prompt_label.place(x=20, y=150)

# Punchline Label
punch_string = StringVar()
punch_label = ttk.Label(root, textvariable=punch_string, font=("Courier", 20), wraplength=480)
punch_label.place(x=20, y=300)

# Next Button
next_button = ttk.Button(root, text="Next", command=next_question)

root.protocol("WM_DELETE_WINDOW", exit)  # Exit program on window close
root.after(2000, main)  # Run main after 2 seconds
root.mainloop()
