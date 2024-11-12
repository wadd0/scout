import time
from typing import Literal

import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information for a city."""
    time.sleep(2)
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's 20 degrees and sunny"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]
model = ChatOpenAI(
    name="gpt-4o-mini",
    temperature=0,
    api_key=st.secrets["OPENAI_API_KEY"],
)
final_model = ChatOpenAI(
    name="gpt-4o-mini",
    temperature=0,
    api_key=st.secrets["OPENAI_API_KEY"],
)

model = model.bind_tools(tools)
# NOTE: this is where we're adding a tag that we'll can use later to filter the model stream events to only the model called in the final node.
# This is not necessary if you call a single LLM but might be important in case you call multiple models within the node and want to filter events
# from only one of them.
final_model = final_model.with_config(tags=["final_node"])
tool_node = ToolNode(tools=tools)


def should_continue(state: MessagesState) -> Literal["tools", "final"]:
    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return "final"


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


def call_final_model(state: MessagesState):
    messages = state["messages"]
    last_ai_message = messages[-1]
    response = final_model.invoke(
        [
            SystemMessage("Rewrite this in the voice of Al Roker"),
            HumanMessage(last_ai_message.content),
        ]
    )
    # overwrite the last AI message from the agent
    response.id = last_ai_message.id
    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)
# add a separate final node
builder.add_node("final", call_final_model)

builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    should_continue,
)

builder.add_edge("tools", "agent")
builder.add_edge("final", END)

graph = builder.compile()


def stream_last_node(prompt):
    # TODO can I run a spinner until hitting the final node?
    inputs = {"messages": [HumanMessage(content=prompt)]}
    for msg, metadata in graph.stream(inputs, stream_mode="messages"):
        if (
            msg.content
            and not isinstance(msg, HumanMessage)
            and metadata["langgraph_node"] == "final"
        ):
            yield msg.content


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
        st.empty()

# Accept user input
if prompt := st.chat_input():
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Answering your question..."):
            response = st.write_stream(stream_last_node(prompt))
            st.empty()
        st.session_state.messages.append({"role": "assistant", "content": response})

# https://discuss.streamlit.io/t/streamlit-spinner-and-chat-message-odd-interaction/82537
# https://discuss.streamlit.io/t/ghost-double-text-bug/68765/6
# https://python.langchain.com/docs/how_to/streaming/#event-reference
