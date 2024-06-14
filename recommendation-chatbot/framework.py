# import requests
# import json
# import gradio as gr

# url = "http://localhost:11434/api/generate"

# headers = {
#     'Content-Type': 'application/json',
# }

# conversation_history = []

# def generate_response(prompt):
#     conversation_history.append(prompt)

#     full_prompt = "\n".join(conversation_history)

#     data = {
#         "model": "moneysaver",
#         "stream": False,
#         "prompt": full_prompt,
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(data))

#     if response.status_code == 200:
#         response_text = response.text
#         data = json.loads(response_text)
#         actual_response = data["response"]
#         conversation_history.append(actual_response)
#         return actual_response
#     else:
#         print("Error:", response.status_code, response.text)
#         return None
    


# demo = gr.Interface(
#     fn=generate_response,
#     inputs="text",
#     outputs="text"
# )

# demo.launch()

import gradio as gr
import random
import time
import json
import requests

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        data = {
                    "model": "moneysaver",
                    "stream": False,
                    "prompt": message,
                }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        bot_message = json.loads(response.text)["response"]
        chat_history.append((message, bot_message))
        time.sleep(2)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()
