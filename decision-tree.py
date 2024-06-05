import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from textblob import TextBlob

# Load the cleaned card transaction data
file_path = 'data/cleaned_card_data.csv'
card_data = pd.read_csv(file_path)

# Convert date columns to datetime
card_data['cpd_dt'] = pd.to_datetime(card_data['cpd_dt'])

# Select relevant features and the target variable
features = card_data[['cluster_name_adjusted', 'mrch_catg_cd', 'domestic_flag', 'intraregion_flag', 'interregion_flag', 'mrch_catg_rlup_nm', 'merchant', 'city_name', 'country_code']]
target = card_data['spend'] * 0.8  # set the "goal" spend as 10% less than the actual spend

# One-hot encode categorical variables
features = pd.get_dummies(features, columns=['cluster_name_adjusted', 'mrch_catg_cd', 'mrch_catg_rlup_nm', 'merchant', 'city_name', 'country_code'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize and train the Decision Tree Regressor
decision_tree = DecisionTreeRegressor(random_state=42)
decision_tree.fit(X_train, y_train)

# Get user input
country = input("Enter your country: ")
persona = input("Enter your persona: ")
description = input("Enter a description of what the money was spent on: ")

# Perform sentiment analysis on the description
sentiment = TextBlob(description).sentiment.polarity

# Add the user input and sentiment to the features
user_features = pd.DataFrame({'cluster_name_adjusted': [persona], 'domestic_flag': [1 if country == 'domestic' else 0], 'intraregion_flag': [0], 'interregion_flag': [0], 'sentiment': [sentiment], 'city_name': ['unknown'], 'country_code': [country]})
user_features = pd.get_dummies(user_features)

# Make sure the user features has the same columns as the training features
missing_cols = set(features.columns) - set(user_features.columns)
for c in missing_cols:
    user_features[c] = 0
user_features = user_features[features.columns]

# Predict the optimal price that the user should be aiming to spend
predicted_spend = decision_tree.predict(user_features)

print(f"The optimal price that you should be aiming to spend is: {predicted_spend[0]}")