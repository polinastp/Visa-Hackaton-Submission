import pandas as pd
import ollama

# Load the CSV file
csv_data = pd.read_csv('data/cleaned_card_data.csv')


# Format CSV data for the SYSTEM message
csv_summary = csv_data.head().to_dict(orient='records')
csv_context = "\n".join([f"{key}: {value}" for record in csv_summary for key, value in record.items()])

# Create the SYSTEM message
system_message = f"""
You are an assistant to the common public, this includes people from all the working class- lower, middle or upper class. Your job is to help optimise
the financial spending of the public. You have access to the following credit card data and your job is to analyse the data and then use this data to give 
insights to the public on how they can optimise their spending. Furthermore, to enhance the experience of the public, you can also provide insights on energy consumption
and how much money they will project to spend in the future, given that they continue to spend at the same rate. Remember to be realistic in your
projections and insights.

I want the responses to be around 50 to 100 words and keep your response as precise to the point as possible.

Here is the credit card data:
{csv_context}
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


