################################
# author: Ohannes (Hovig) Ohannessian
# file: score_model.py gets & outputs prediction, accuracy score, confusion matrix
#        & classification report on model.pkl, X_test.csv, y_test.csv & test.csv
################################

# Import needed libraries
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import pickle

def read_pickle_model(file):
    try:
        # Open the model pickle file and make its content available
        p = open(file, 'rb')
        open_pkl = pickle.load(p)
    except:
        # Display error message if there's error opening the file
        print("Issue opening", file)
    return(open_pkl)

def get_test_df(df):
    # Convert from categorical variables into dummy variables and drop columns
    df = df.drop(['PassengerId', 'Name', 'Cabin', 'Ticket'], axis=1)
    dum = pd.get_dummies(df)
    dum = dum.drop(['Sex_female', 'Embarked_C'], axis=1)
    return(dum)

# Read and assign files to variables
test_df = pd.read_csv("test.csv")
X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv")

# Drop columns
X_test.drop(X_test.columns[[0]], axis=1, inplace=True)
y_test.drop(y_test.columns[[0]], axis=1, inplace=True)
X_test.drop(X_test.index[0], inplace=True)

# Get the pickle file for the model
model = read_pickle_model('model.pkl')

# Get the score of the model
accuracy_score = model.score(X_test, y_test)

# Modify test content
pred_df = get_test_df(test_df)

# Run prediction on X_test
y_pred = model.predict(X_test)

# Run prediction on test
test_pred = model.predict(pred_df)

# Generate classification report
class_report = classification_report(y_test, y_pred)

# Generate confusion matrix
conf_mat = confusion_matrix(y_test, y_pred)

# Display outputs
print("\n* Model accuracy score:")
print(accuracy_score)
print("\n* Model confusion matrix:")
print(*conf_mat, sep = ' ')
print("\n* Classification report:\n")
print(class_report)
print("\n* Test model predictions:")
print(*test_pred, sep = ' ')
