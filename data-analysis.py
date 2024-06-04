import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/cleaned_card_data.csv")


def persona_analysis(data):
    persona_summary = data.groupby('cluster_name_adjusted').agg({
        'spend': ['sum', 'mean', 'count'],
        'mrch_catg_cd': 'nunique'
    }).reset_index()
    persona_summary.columns = ['Persona', 'Total Spend', 'Average Spend', 'Transaction Count', 'Unique Merchant Categories']
    print(persona_summary)


# def energy_consumption_insights(data):
#     energy_categories = [4812, 5815, 5734, 5732, 4900, 5816]  # energy-related transactions
#     energy_data = data[data['mrch_catg_cd'].isin(energy_categories)].copy()
#     energy_data = energy_data.dropna(subset=['cpd_dt'])
#     energy_data.loc[:, 'cpd_dt'] = pd.to_datetime(energy_data['cpd_dt'], format='%Y-%m-%d', errors='coerce')
#     energy_data = pd.get_dummies(energy_data, columns = ['cluster_name_adjusted', 'mrch_catg_cd', 'mrch_catg_rlup_nm', 'merchant', 'city_name', 'country_code'])
#     energy_summary = energy_data.groupby(['cpd_dt'], as_index=False).mean()
#     energy_summary['Month'] = energy_summary['cpd_dt'].dt.strftime('%Y-%m')
#     energy_summary = energy_summary[['Month', 'spend']]  # select the columns you're interested in
#     energy_summary.columns = ['Month', 'Total Energy Spend']
#     print(energy_summary)
def energy_consumption_insights(data):
    energy_categories = [4812, 5815, 5734, 5732, 4900, 5816]  # energy-related transactions
    energy_data = data[data['mrch_catg_cd'].isin(energy_categories)].copy()
    energy_data = energy_data.dropna(subset=['cpd_dt'])
    energy_data.loc[:, 'cpd_dt'] = pd.to_datetime(energy_data['cpd_dt'], format='%Y-%m-%d', errors='coerce')
    energy_data = pd.get_dummies(energy_data, columns = ['cluster_name_adjusted', 'mrch_catg_cd', 'mrch_catg_rlup_nm', 'merchant', 'city_name', 'country_code'])
    energy_summary = energy_data.groupby(['cpd_dt'], as_index=False).mean()
    energy_summary['Total Transaction Count'] = energy_data.groupby(['cpd_dt']).size().values  # add the new column
    energy_summary['Date'] = energy_summary['cpd_dt'].dt.strftime('%Y-%m-%d')
    energy_summary = energy_summary[['Date', 'spend', 'Total Transaction Count']]  # select the columns you're interested in
    energy_summary.columns = ['Date', 'Total Energy Spend', 'Total Transaction Count']
    print(energy_summary)

def financial_insights(data):
    financial_summary = data.groupby(data['cpd_dt']).agg({
        'spend': ['sum', 'mean', 'count'],
        'mrch_catg_cd': 'nunique'
    }).reset_index()
    financial_summary.columns = ['Month', 'Total Spend', 'Average Spend', 'Transaction Count', 'Unique Merchant Categories']
    print(financial_summary)


persona_analysis(df)
energy_consumption_insights(df)
financial_insights(df)
