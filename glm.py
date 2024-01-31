import streamlit as st
import os
import json, ast
import requests
from zhipuai import ZhipuAI


if "key" not in st.session_state:
    st.session_state.key = None
    
key = st.sidebar.text_input("Your key", type="password") 
model=st.sidebar.selectbox(
    'Model',
    ('glm-3-turbo', 'glm-4', 'glm-4v'))

if not key:
    st.info("Please add your key to continue.")
else:
    st.session_state.key=key    



if not key:
    st.stop()
  
def run_conversation(prompt,feedback):
    messages = [{"role":"system","content":'''You are an assistant and good at answering any questions.
    '''}]
    
    for msg in st.session_state.messages[-15:]:
        if msg["role"]=="user":
            messages.append({ "role": "user","content": msg["content"]})
        elif msg is not None and msg["content"] is not None:
            messages.append({ "role": "assistant", "content":msg["content"]})
    
    print(messages)
    client = ZhipuAI(api_key=st.session_state.key) 
    response = client.chat.completions.create(
        model=model,  # 填写需要调用的模型名称
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        stream=True
    )
    
    ret=''
    for chunk in response:
        
        if chunk.choices:
            print(chunk.choices)
            if chunk.choices[0].delta.content:
                c=chunk.choices[0].delta.content
                ret+=c
                feedback(ret)
            
    return ret


if "messages" not in st.session_state:
    st.session_state.messages = []

    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def writeReply(cont,msg):
    cont.write(msg)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        p=st.empty()
        p.write("Thinking...")
        re = run_conversation(prompt,lambda x:writeReply(p,x))
        print(re)
        st.session_state.messages.append({"role": "assistant", "content": re})
