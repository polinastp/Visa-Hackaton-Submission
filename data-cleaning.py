import pandas as pd

# Load the card transaction data
file_path = 'data/Visa Climate Tech Data.xlsx - 2_Card data.csv'
card_data = pd.read_csv(file_path)

# Convert date columns to datetime
card_data['cpd_dt'] = pd.to_datetime(card_data['cpd_dt'], format='%m/%d/%Y')

# Handle missing values by forward filling
card_data.fillna(method='ffill', inplace=True)

# Remove duplicates if any
card_data.drop_duplicates()

# Ensure consistency in categorical variables
# categorical_columns = ['cluster_name_adjusted', 'mrch_catg_cd', 'mrch_catg_rlup_nm', 'merchant', 'city_name', 'country_code']
# for column in categorical_columns:
#     card_data[column] = card_data[column].astype('category')

# Save cleaned data
card_data.to_csv('data/cleaned_card_data.csv')

print("Data preparation is complete. Cleaned data saved to 'cleaned_card_data.csv'.")
