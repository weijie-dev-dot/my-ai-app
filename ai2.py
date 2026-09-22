import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="ai chat", layout="wide", initial_sidebar_state="expanded")
st.title("ai chat")
system_prompt = "You are a helpful assistant"
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    elif message["role"] == "assistant":
        st.chat_message("assistant").write(message["content"])

client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")

prompt = st.chat_input("Your problem")
if prompt:
    st.chat_message("user").write(prompt)
    print("------>提示词：", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 输出的结果
    response_message=st.empty()
    full_response=""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content=chunk.choices[0].delta.content
            full_response += content
            st.chat_message("assistant").write(full_response)



    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

