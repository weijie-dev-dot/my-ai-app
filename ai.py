#
import os
from openai import OpenAI
import streamlit as st
st.session_state.messages = []  # 👈 强行清空历史记录！
st.set_page_config(page_title="ai",layout="wide",initial_sidebar_state="expanded")
st.title("ai")
# 显示信息
if "messages" in st.session_state:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assisant").write(message["content"])


client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

system_prompt ="你是一个乖宝宝"
st.session_state.messages = []  # 👈 强行清空所有历史脏数据
if "messages" not in st.session_state:
    st.session_state.messages = []

prompt=st.chat_input("Your problem")

if prompt:
    # 1. 把用户的话存入历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. 准备发送给AI的消息列表（把系统提示和历史记录拼起来）
    messages_to_send = [{"role": "system", "content": system_prompt}]
    messages_to_send.append({"role": "user", "content": prompt})  # 👈 强行把当前问题加进去
    messages_to_send.extend(st.session_state.messages)  # 再把历史记录加进去
    # 3. 发送请求（去掉多余的参数）
    with st.chat_message("assistant"):
        with st.spinner("乖宝宝思考中..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages_to_send,#type: ignore
                    stream=False
                )
                # 重新渲染历史聊天记录（防止刷新/发送时页面丢记忆）

                ai_reply = response.choices[0].message.content
                st.write(ai_reply)

                # 4. 把AI真正的回答存入历史！
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                st.error(f"出错了: {e}")
    # 输出的结果
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
