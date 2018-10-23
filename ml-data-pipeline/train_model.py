################################
# author: Ohannes (Hovig) Ohannessian
# file: train_model.py reads the downloaded files, runs RandomForestClassifier, outputs
#       trained model in a pickle file & saves the training sets into new csv files
################################

# Import needed libraries
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

def RFC(X, y):
    try:
        # Random Forest Classification and pipeline setup
        imputer = Imputer(missing_values='NaN', strategy='mean', axis=0)
        rfc = RandomForestClassifier(max_depth=10, min_samples_split=2, n_estimators=100, random_state=1)
        steps = [('imputation', imputer), ('random_forest', rfc)]
        pipeline = Pipeline(steps)

        # Create and store into test csv files for X and y
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        X_test.to_csv('X_test.csv')
        y_test.to_csv('y_test.csv')

        # Fit the model
        model = pipeline.fit(X_train, y_train)
    except:
        # Display message if the there's RFC function failure
        print("Check pipeline setup, fit or csv file save.")
    return(model)

# Read the training dataset and drop columns and null
df = pd.read_csv("train.csv")
df = df.drop(['Name', 'Cabin', 'Ticket'], axis=1)
df = df.dropna(subset=['Embarked'], how='all')

# Convert from categorical variables into dummy variables and drop columns
dum = pd.get_dummies(df)
dum = dum.drop(['Sex_female', 'Embarked_C'], axis=1)

# Assignment and non-assignment of columns for X and y
y = dum['Survived']
X = dum.drop('Survived', axis=1)

# Pass in values for random forest classification, create pipeline and fit model
model = RFC(X,y)

# Create and store into pickle file the fit model from random forest classifier
p = open('model.pkl', 'wb')
pickle.dump(model, p)
p.close()
