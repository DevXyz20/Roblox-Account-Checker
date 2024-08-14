from flask import Flask, request
from threading import Thread
import requests
import json
import colorama
from colorama import Fore, Style
from datetime import datetime
import time

colorama.init()

app = Flask('')

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>rospeed checker  V1.0</title>
    <style>
        body {
            background-color: black;
            color: green;
            text-align: center;
        }
        h1 {
            font-size: 3em;
            font-family: monospace;
            animation: moveText 3s infinite;
        }
        @keyframes moveText {
            0% { color: white; }
            25% { color: black; }
            50% { color: green; }
            75% { color: yellow; }
            100% { color: white; }
        }
        input[type="text"], input[type="submit"] {
            margin: 10px;
            padding: 5px;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <h1>Ro speed 2 Checker  v1.0</h1>
    <form action="/check" method="post">
        <label for="account_id">Enter Account ID:</label><br>
        <input type="text" id="account_id" name="account_id"><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/check', methods=['POST'])
def check_account():
    account_id = request.form['account_id']
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{Style.BRIGHT}[{Fore.WHITE}{current_time}{Style.RESET_ALL}] {Style.BRIGHT}{Fore.WHITE}Checking...{Style.RESET_ALL}")

    # Simulate a delay of 5 seconds
    time.sleep(5)

    account_info = check_roblox_account(account_id)

    if account_info:
        followers = get_followers(account_id) or []
        following = get_following(account_id) or []
        friends_count, friends_names = get_friends(account_id)
        print(f"\n{Style.BRIGHT}[{Fore.WHITE}{current_time}{Style.RESET_ALL}] {Style.BRIGHT}{Fore.GREEN}Successful! The account has been checked{Style.RESET_ALL}")
        save_account_info(account_info, followers, following, friends_count, friends_names)
        return f"<h1>{current_time} - Successful! The account has been checked.</h1><h2 style='color: yellow;'>The Tool By instagram: xyzrich.a discord: discord.gg/freeservice</h2>"
    else:
        print(f"\n{Style.BRIGHT}[{Fore.WHITE}{current_time}{Style.RESET_ALL}] {Style.BRIGHT}{Fore.RED}Failed to check the account. Please try again. The account banned or not found{Style.RESET_ALL}")
        return f"<h1>{current_time} - Failed to check the account. Please try again. The account banned or not found.</h1>"

def check_roblox_account(account_id):
    url = f"https://users.roblox.com/v1/users/{account_id}"
    response = requests.get(url)
    if response.status_code == 200:
        account_info = response.json()
        return account_info
    else:
        return None

def get_followers(account_id):
    url = f"https://friends.roblox.com/v1/users/{account_id}/followers"
    response = requests.get(url)
    if response.status_code == 200:
        followers_info = response.json()
        followers_names = [follower['name'] for follower in followers_info['data']]
        return followers_names
    else:
        return None

def get_following(account_id):
    url = f"https://friends.roblox.com/v1/users/{account_id}/followings"
    response = requests.get(url)
    if response.status_code == 200:
        following_info = response.json()
        following_names = [follow['name'] for follow in following_info['data']]
        return following_names
    else:
        return None

def get_friends(account_id):
    url = f"https://friends.roblox.com/v1/users/{account_id}/friends/count"
    response = requests.get(url)
    if response.status_code == 200:
        friends_info = response.json()
        friends_count = friends_info.get('count', 0)
        friends_names = []

        if friends_count > 0:
            friends_url = f"https://friends.roblox.com/v1/users/{account_id}/friends"
            response = requests.get(friends_url)
            if response.status_code == 200:
                friends_data = response.json().get('data', [])
                friends_names = [friend['name'] for friend in friends_data]

        return friends_count, friends_names
    else:
        return 0, []

def save_account_info(account_info, followers, following, friends_count, friends_names):
    with open('info.txt', 'w') as file:
        file.write("Account Info:\n")
        file.write(f"About: {account_info.get('description', 'About information not available.')}\n")
        file.write(f"Map: {account_info.get('location', 'Map information not available.')}\n")
        file.write(f"Date: {account_info.get('created', 'Date information not available.')}\n")
        file.write(f"Followers:\n")
        for follower in followers:
            file.write(f"- {follower}\n")
        file.write(f"Following:\n")
        for followee in following:
            file.write(f"- {followee}\n")
        file.write(f"Friends Count: {friends_count}\n")
        if friends_names:
            file.write("Friends Names:\n")
            for friend in friends_names:
                file.write(f"- {friend}\n")

def main():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
  # just jk
# /0/0 = " O  P  E   N"
# print(/0/0)



