import requests
import pandas as pd
import random as rand

import os
from dotenv import load_dotenv
load_dotenv()
PASS = os.getenv("PASS")

########################### initialise the auth for the bot ###########################
def initialise_bot():
    CLIENT_ID = '_PVY5gJ4bDbpwMYhjv01_Q'
    SECRET_KEY = 'eFYIA6Ox-lloLzkAGgudt-9CEzWVeQ'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    data = {
        'grant_type': 'password',
        'username': 'redditbotaccount984',
        'password': PASS
    }

    #identify our API
    headers = {'User-Agent': 'MyAPI/0.0.1'}

    #send request for token
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth = auth, data=data, headers = headers)

    TOKEN = res.json()['access_token']
    headers['Authorization'] = f'bearer {TOKEN}'
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    
    #return the headers for future API calls
    return headers

# you should have headers=headers in all future API calls
# SAMPLE = requests.get("https://oauth.reddit.com/r/python/hot", headers=headers)
########################### returns headers for future API calls ###########################

#prints a data frame of post info using the given subreddit name and category. Will assume valid inputs (must also send headers)
def get_sub_posts(subname, category, headers):
    res = requests.get("https://oauth.reddit.com/r/" + subname + "/" + category, headers=headers)

    #since df = df.append will be depricated later, we have to create lists and create a df at the end
    subreddits = []
    titles = []
    selftext = []
    upvote_ratio = []
    ups = []
    downs = []
    score = []

    # loop through each post retrieved from GET request
    for post in res.json()['data']['children']:
        # append relevant data to dataframe

        subreddits.append(post['data']['subreddit'])
        titles.append(post['data']['title'])
        selftext.append(post['data']['selftext'])
        upvote_ratio.append(post['data']['upvote_ratio'])
        ups.append(post['data']['ups'])
        downs.append(post['data']['downs'])
        score.append(post['data']['score'])

    df = pd.DataFrame({
        'subreddit': subreddits,
        'title' : titles,
        'selftext' : selftext,
        'upvote_ratio' : upvote_ratio,
        'ups' : ups,
        'downs' : downs,
        'score' : score
    })

    print(df)
########################### code to be put in the main func ###########################
# subreddit = input('Enter the subreddit name: ')
# category = input('Enter the category you want to see (hot,new,rising): ')
# get_sub_posts(subreddit, category, headers=headers)
########################### paste this^^^ in the main function (needs authentication to run) ###################

#class to hold subreddit name and sub count
class sub_summary:
    def __init__(self, sub_name, sub_count):
        self.subreddit = sub_name
        self.subscribers = int(sub_count)

    def __repr__(self) -> str:
        return "{}: {}".format(self.subreddit, self.subscribers)
    

#prints and writes to a file all the subreddits that the api could get me
def get_subreddits(headers):
    base_url = 'https://oauth.reddit.com/reddits.json'

    all_subreddits = []

    #interesting to note that nsfw subreddits (18+) are not recorded

    response = requests.get('https://oauth.reddit.com/reddits.json', headers = headers)
    raw_data = response.json()["data"]["children"]

    #for each subreddit (stored in raw_data), get their names and sub counts
    global count
    count = 0

    open("list of subs.txt", "w").close() #clears the textfile first
    file = open("list of subs.txt", "a")

    def get_info(raw_data):
        for subreddit in raw_data:
            name = subreddit["data"]['display_name']
            subscribers = subreddit["data"]['subscribers']
            all_subreddits.append(sub_summary(name, subscribers))
            global count
            count += 1
            #we utilize the fact that count is a thing to keep paging thru the reddit api

            print("{}: {}".format(name, subscribers))
            file.write("{}: {}\n".format(name, subscribers))

            if(count % 25 == 0): #if we reach the page limit, go next
                last_subreddit = subreddit["data"]['name']
                url_addon = "?count={}&after={}".format(count,last_subreddit)

                #this generates a new request
                response = requests.get(base_url+url_addon, headers = headers)
                raw_data = response.json()["data"]["children"]
                get_info(raw_data)

    get_info(raw_data)

    file.close()
########################### code to be put in the main func ###########################
# goes through as many subs as it can (4088) and returns their name and sub count (u can do more with this if u add fields to get)
# needs valid headers to work
########################### paste this^^^ in the main function (needs authentication to run) ###################

########################### MERGE SORT (Decreasing order) ###########################
def mergeSort(arr): #takes in a list of sub_summary objects
    if len(arr) > 1:
        # Finding the mid of the array
        mid = len(arr)//2
        # Dividing the array elements
        L = arr[:mid]
        # into 2 halves
        R = arr[mid:]
  
        # Sorting the first half
        mergeSort(L)
  
        # Sorting the second half
        mergeSort(R)
  
        i = j = k = 0
  
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i].subscribers > R[j].subscribers:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
  
        # Checking if any element were left over
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
  
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

########################### merge sorts a list of sub_summarys ###########################

########################### reads sub_summarys from filename and puts them in sub data ###########################
def into_list(sub_data, filename):
    raw_data = open(filename, "r")
    for line in raw_data:
        split = line.split(": ")
        data_pt = sub_summary(split[0], split[1])
        sub_data.append(data_pt)
    raw_data.close()
########################### use this to initialize your list ###########################

########################### writes a list to a file ###########################
def print_to_file(list, filename):
    #clear the file first
    open(filename, "w").close()

    file = open(filename, "a")
    for entry in list:
        file.write(repr(entry) + "\n")
    file.close()
########################### use this to write list to files for better display ###########################

#################################################### These are helper functions for running the game ####################################################

#returns a boolean result of the user's resp
def handle_response(resp, first, second):
    #make sure the response you get wont brick the game
    while resp != "1" and resp != "2":
        print("Please enter a valid response!\n")
        resp = input("Which subreddit has more members? (1 or 2): ")
    
    answer = -1
    if first.subscribers > second.subscribers:
        answer = 1
    else:
        answer = 2

    return (answer == int(resp))

#returns a random subreddit
def get_rand_sub(length, sub_list):
    index = rand.randint(0, length-1)
    return sub_list[index]

#makes sure the second subreddit is different than the first
def ensure_difference(length, sub_list, first, second):
    while(first == second):
        second = get_rand_sub(length,sub_list)
########################### These are helper functions for running the game ###########################


########################### This is the code to run the higher or lower game ###########################

#game start function
def game_start(sub_data):
    score = 0

    print("Game Start!\n")
    #pick a random entry from sub_data
    num_subs = len(sub_data)
    first_sub = get_rand_sub(num_subs, sub_data)
    print("1: " + first_sub.subreddit + ", {}\n".format(first_sub.subscribers))

    #pick the second sub
    second_sub = get_rand_sub(num_subs, sub_data)
    ensure_difference(num_subs, sub_data, first_sub, second_sub)
    print("2: " + second_sub.subreddit + "\n")

    resp = input("Which subreddit has more members? (1 or 2): ")
    result = handle_response(resp, first_sub, second_sub)

    if(not result): #the guess was wrong
        print("Incorrect! {} has {} subscribers".format(second_sub.subreddit, second_sub.subscribers))
        print("Game Over, your score: {}".format(score))
    
    else:           #the guess was right! continue the game
        while(result):
            score +=1
            print("Correct! Your score: {}\n".format(score))
            result = False

            #generate new subreddit
            first_sub = second_sub
            print("1: " + first_sub.subreddit + ", {}\n".format(first_sub.subscribers))
            second_sub = get_rand_sub(num_subs, sub_data)
            ensure_difference(num_subs, sub_data, first_sub, second_sub)
            print("2: " + second_sub.subreddit + "\n")

            resp = input("Which subreddit has more members? (1 or 2): ")
            result = handle_response(resp, first_sub, second_sub)
        
        #player has died
        print("Incorrect! {} has {} subscribers".format(second_sub.subreddit, second_sub.subscribers))
        print("Game Over, your score: {}".format(score))
        #END OF GAME#

########################### Pass in a list of sub_summaries ###########################