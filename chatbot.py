import streamlit as st
import time
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    api_key=st.secrets["OPENAI_API_KEY"],
    streaming=True,
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{prompt}"),
    ]
)

chain = chat_prompt | llm


# agent_executor = create_react_agent(model, tools)

# TODO create agent with tools to answer the question...

st.title("Scout Assistant")

with st.expander("Info"):
    st.markdown("# Heading \n Body.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me a question about Scouts"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        cfg = RunnableConfig()
        cfg["callbacks"] = [st_cb]
        response = st.write_stream(
            chain.stream(
                {
                    "messages": st.session_state.messages,
                    "prompt": prompt,
                    "config": cfg,
                }
            )
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
