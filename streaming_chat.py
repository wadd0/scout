import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from agent.agent import stream_scout_agent


st.title("Scout")

st.warning("This is a warning...", icon="⚠️")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [AIMessage("How can I help you?")]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)


# Accept user input
if prompt := st.chat_input("Message"):
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=prompt))
    # Display user message in chat message container
    with st.chat_message("human"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("ai"):
        placeholder = st.empty()
        # Display spinner while waiting
        placeholder.image("assets/3-dots-scale.svg")
        response = placeholder.write_stream(
            stream_scout_agent(st.session_state.messages)
        )
    st.session_state.messages.append(AIMessage(response))
