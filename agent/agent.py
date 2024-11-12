from langchain_core.messages import AIMessageChunk, BaseMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.risk.assessment import risk_assessment_tool


# TODO this should be imported form search
@tool
def search(search: str):
    """Search for information."""
    return f"I don't know the answer to: {search}."


tools = [search, risk_assessment_tool]

# TODO the model should be dynamic
model = ChatOpenAI(model="gpt-4o-mini", streaming=True)

system = SystemMessage(
    content=(
        "You are a helpful assistant. Answer questions using ONLY the conversation "
        "context and tools available to you. Avoid using your own knowledge. "
        "If you don't know the answer then say so."
        "Use plain British english and commonly used terms in your response."
        "Your tone should be formal."
    )
)
react_agent = create_react_agent(model, tools=tools, state_modifier=system)


def stream_scout_agent(messages: list[BaseMessage]):
    for msg, _ in react_agent.stream({"messages": messages}, stream_mode="messages"):
        if isinstance(msg, AIMessageChunk):
            yield msg
