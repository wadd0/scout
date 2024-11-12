from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class State(TypedDict):
    input: str
    user_feedback: str
    llm: str


def step_1(state):
    print("---Step 1---")
    pass


def human_feedback(state):
    print("---human_feedback---")
    response = model.invoke(state["input"])
    return {"user_feedback": response.content}


def step_3(state):
    print("---Step 3---")
    response = model.invoke(state["user_feedback"])
    return {"llm": response.content}


def router(state):
    if state["user_feedback"] == "end":
        return END
    return "step_1"


builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_conditional_edges("step_3", router)
# builder.add_edge("step_3", END)

# Set up memory
memory = MemorySaver()

# Add
graph = builder.compile(checkpointer=memory, interrupt_before=["human_feedback"])


# Input
graph_input: dict | None = {"input": "hello world"}

# Thread
config = RunnableConfig()
config["configurable"] = {"thread_id": "1"}

# for event in graph.stream(graph_input, config, stream_mode="values"):
#     print(graph.get_state(config))
#     print(event)

# graph_input = input("Tell me how you want to update the state: ")

# graph.update_state(config, {"user_feedback": graph_input}, as_node="human_feedback")

# for event in graph.stream(None, config, stream_mode="values"):
#     print(graph.get_state(config))
#     print(event)

# while True:

#     for event in graph.stream(graph_input, config, stream_mode="values"):
#         print(event)

#     next_node = graph.get_state(config).next
#     # Has this graph terminated?
#     if next_node:
#         user_input = input("Tell me how you want to update the state: ")
#         graph.update_state(
#             config,
#             {"user_feedback": user_input},
#             as_node="human_feedback",
#         )
#         graph_input = None
#     else:
#         break

# should this be just simpler to interact with streamlit
# this returns a question to be answered ot the answer

print(graph.invoke(graph_input, config))

# to simplify streamlit, send the graph one message at a time plus an ID
# the graph can maintain it's own state and return a question to the user
# human then sends a human message with ID back to the graph...
