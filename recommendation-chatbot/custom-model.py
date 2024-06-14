# import pandas as pd
# import ollama


# def csv2context(csv_data):
#     # Format CSV data for the SYSTEM message
#     csv_summary = csv_data.head().to_dict(orient='records')
#     csv_context = "\n".join([f"{key}: {value}" for record in csv_summary for key, value in record.items()])
#     return csv_context

# card = csv2context(pd.read_csv('data/cleaned_card_data.csv'))
# energy = csv2context(pd.read_csv('data/energy_consumption_insights.csv'))
# financial = csv2context(pd.read_csv('data/financial_insights.csv'))
# persona = csv2context(pd.read_csv('data/persona_analysis.csv'))

# # Create the SYSTEM message
# system_message = f"""
# You are an assistant to the common public, this includes people from all the working class- lower, middle or upper class. Your job is to help optimise
# the financial spending of the public. You have access to the following credit card data and your job is to analyse the data and then use this data to give 
# insights to the public on how they can optimise their spending. Furthermore, to enhance the experience of the public, you can also provide insights on energy consumption
# and how much money they will project to spend in the future, given that they continue to spend at the same rate. Remember to be realistic in your
# projections and insights.

# I want the responses to be no more than 50 to 100 words and keep your response as precise to the point as possible.

# Here is the credit card data. I cannot stress enough how important it is to note that these data is only generic and not directed to any individual or entity. Use 
# this data as a means of benchmark and use it wisely to give insights:
# {card}
# {energy}
# {financial}
# {persona}

# Use the data above as a means to give insights but in your responses do not included any statistics from the mentioned data.
# """

# # Define the modelfile with the updated SYSTEM message
# modelfile_content = f"""
# FROM llama3
# PARAMETER temperature 1
# SYSTEM "{system_message}"
# TEMPLATE "{{{{ if .System }}}}system
# {{{{ .System }}}}{{{{ end }}}}{{{{ if .Prompt }}}}user
# {{{{ .Prompt }}}}{{{{ end }}}}assistant
# {{{{ .Response }}}}"
# """

# # Create and run the model using the Ollama library
# ollama.create(model='moneysaver', modelfile=modelfile_content)

### THE FOLLOWING CODE UPDATES THE MODEL EVERY HOUR IN CASE THERES DYNAMIC CHANGES TO CSV ###
import pandas as pd
import ollama
import schedule
import time

def csv2context(csv_data):
    # Format CSV data for the SYSTEM message
    csv_summary = csv_data.head().to_dict(orient='records')
    csv_context = "\n".join([f"{key}: {value}" for record in csv_summary for key, value in record.items()])
    return csv_context

def update_model():
    card = csv2context(pd.read_csv('data/cleaned_card_data.csv'))
    energy = csv2context(pd.read_csv('data/energy_consumption_insights.csv'))
    financial = csv2context(pd.read_csv('data/financial_insights.csv'))
    persona = csv2context(pd.read_csv('data/persona_analysis.csv'))

    # Create the SYSTEM message
    system_message = f"""
    You are an assistant to the common public, this includes people from all the working class- lower, middle or upper class. Your job is to help optimise
    the financial spending of the public. You have access to the following credit card data and your job is to analyse the data and then use this data to give 
    insights to the public on how they can optimise their spending. Furthermore, to enhance the experience of the public, you can also provide insights on energy consumption
    and how much money they will project to spend in the future, given that they continue to spend at the same rate. Remember to be realistic in your
    projections and insights.

    I want the responses to be no more than 50 to 100 words and keep your response as precise to the point as possible.

    Here is the credit card data. I cannot stress enough how important it is to note that these data is only generic and not directed to any individual or entity. Use 
    this data as a means of benchmark and use it wisely to give insights:
    {card}
    {energy}
    {financial}
    {persona}

    Use the data above as a means to give insights but in your responses do not included any statistics from the mentioned data.
    """

    # Define the modelfile with the updated SYSTEM message
    modelfile_content = f"""
    FROM llama3
    PARAMETER temperature 1
    SYSTEM "{system_message}"
    TEMPLATE "{{{{ if .System }}}}system
    {{{{ .System }}}}{{{{ end }}}}{{{{ if .Prompt }}}}user
    {{{{ .Prompt }}}}{{{{ end }}}}assistant
    {{{{ .Response }}}}"
    """

    # Create and run the model using the Ollama library
    ollama.create(model='moneysaver', modelfile=modelfile_content)
    print("Model updated successfully.")

# Schedule the update_model function to run every hour
schedule.every().hour.do(update_model)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
