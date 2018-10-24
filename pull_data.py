################################
# author: Ohannes (Hovig) Ohannessian
# file: pull_data.py takes in user's username & password from console, request calls to login into kaggle
#          and to download the 2 titanic datasets - train.csv and test.csv
################################

# Import needed libraries
import os, getpass, requests
import pandas as pd
from score_model import display
from flask import Flask, request
from pathlib import Path

main_page = '''
<html>
    <head>
    <title></title>
    <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css">
    </head>
<body>
<form class="form-horizontal" method="post" action="/calc">
<fieldset>

<!-- Form Name -->
<legend><center>Python Machine Learning Data Pipeline</center></legend>

<!-- Text input-->
<div class="form-group">
  <center><p>If there are problems querying the Kaggle APIs or if CSV files exist, click on Import button to bypass login credentials.</p></center><br>
  <label class="col-md-4 control-label" for="textinput">Kaggle Credentials:</label>
  <div class="col-md-4">
  <input name="textinput1" id="textinput" type="text" placeholder="Enter username" class="form-control input-md">
  <input name="textinput2" id="textinput" type="password" placeholder="Enter passsword" class="form-control input-md">
  </div>
</div>

<!-- Button -->
<div class="form-group">
  <label class="col-md-4 control-label" for="singlebutton"></label>
  <div class="col-md-4" align="center">
    <button id="singlebutton" name="singlebutton" class="btn btn-primary">Import</button>
  </div>
</div>

</fieldset>
</form>
<script src="http://netdna.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

app = Flask(__name__)
app.config['Debug'] = True

PORT = int(os.getenv('PORT', 5000))

@app.route('/')
def index():
     return main_page.format('')

@app.route("/calc", methods=['POST'])
def calc():
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

    if request.method == 'POST':
        f = Path("test.csv")
        if not f.is_file():
            user = str(request.form['textinput1'])
            passwd = str(request.form['textinput2'])

            # Kaggle URLs for downloading Titanic datasets
            loginURL = "https://www.kaggle.com/account/login"
            dataURL = "https://www.kaggle.com/c/3136/download/train.csv"

            # Working with training and testing csv files
            filename = ['train.csv', 'test.csv']

            # Pass in to pull_datasets function the values needed to download the datasets
            pull_datasets(filename[0], loginURL, dataURL, user, passwd)
            pull_datasets(filename[1], loginURL, dataURL, user, passwd)

        # Run the next 2 files after the downloads are done
        os.system('python train_model.py')
        os.system('python score_model.py')
        print(">>>",display)
        return display
    else:
        return 'Error!'

if __name__ == '__main__':
    app.run(debug=True, port=PORT, host='0.0.0.0')
