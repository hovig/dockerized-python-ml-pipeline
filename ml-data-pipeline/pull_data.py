################################
# author: Ohannes (Hovig) Ohannessian
# file: pull_data.py takes in user's username & password from console, request calls to login into kaggle
#          and to download the 2 titanic datasets - train.csv and test.csv
################################

# Import needed libraries
import os, getpass, requests
import pandas as pd

def pull_datasets(filename, loginURL, dataURL, user, passwd):
    # Kaggle user payload credentials for API access
    # https://stackoverflow.com/questions/50863516/issue-in-extracting-titanic-training-data-from-kaggle-using-jupyter-notebook
    payload = {
        '__RequestVerificationToken': '',
        'username': user,
        'password': passwd,
        'rememberme': 'false'
    }

    with requests.Session() as c:
        # Get token and assign to __RequestVerificationToken
        response = c.get(loginURL).text
        AFToken = response[response.index('antiForgeryToken')+19:response.index('isAnonymous: ')-12]
        print("AntiForgeryToken={}".format(AFToken))
        payload['__RequestVerificationToken']=AFToken

        # Get datasets in a callback
        c.post(loginURL + "?isModal=true&returnUrl=/", data=payload)
        response = c.get(dataURL)
        print(response)

        # Save contents into their appropriate csv files
        with open(filename, 'wb') as f:
             f.write(response.content)
             f.close()

# Kaggle URLs for downloading Titanic datasets
loginURL = "https://www.kaggle.com/account/login"
dataURL = "https://www.kaggle.com/c/3136/download/train.csv"

# Take in user's Kaggle username and password without storing them
print("--------------------------------------------------")
print("(Important: First time Kaggle user, download datasets\nmanually from browser to accept Kaggle's terms.)\n")
print("Enter your Kaggle's credentials")
print("-----------------------------------")

user = getpass.getpass("Username: ")
passwd = getpass.getpass("Password: ")

# Working with training and testing csv files
filename = ['train.csv', 'test.csv']

# Pass in to pull_datasets function the values needed to download the datasets
pull_datasets(filename[0], loginURL, dataURL, user, passwd)
pull_datasets(filename[1], loginURL, dataURL, user, passwd)

# Run the next 2 files after the downloads are done
os.system('python train_model.py')
os.system('python score_model.py')
