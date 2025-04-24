import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/chat"  # Make sure this matches your backend

def chat_fn(message, history):
    try:
        payload = {"message": message, "history": history}
        res = requests.post(API_URL, json=payload)
        res.raise_for_status()  # Catch 4xx/5xx HTTP errors

        data = res.json()
        print("🟢 API Response:", data)

        bot_reply = data.get("response", "⚠️ No response returned from server.")
    except requests.exceptions.RequestException as e:
        print("🔴 Server error:", e)
        bot_reply = f"⚠️ Server error: {str(e)}"
    except Exception as e:
        print("🔴 Unexpected error:", e)
        bot_reply = f"⚠️ Unexpected error: {str(e)}"

    history.append((message, bot_reply))
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Chat with AI")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message here...", show_label=False)
    state = gr.State([])
    submit = gr.Button("🚀 Send")

    submit.click(chat_fn, [msg, state], [chatbot, state])
    msg.submit(chat_fn, [msg, state], [chatbot, state])

demo.launch()
