import itertools
import json

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from .models import ExampleRiskAssessment, RiskAssessment
from .prompts import assessment_prompt, user_prompt


# TODO needs config for model etc
def get_examples():
    with open("agent/risk/assessment_examples.json") as f:
        examples = json.load(f)

    examples = [
        ExampleRiskAssessment(**example).to_messages(user_prompt)
        for example in examples
    ]

    return list(itertools.chain(*examples))


# TODO these could come from a cloud bucket using configurable URL for access?
examples = get_examples()


# TODO model should be configurable?
def build_assessment_chain(examples: list[BaseMessage] = examples):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    llm = model.with_structured_output(RiskAssessment)
    chain = assessment_prompt.partial(examples=examples, n_min=7) | llm

    return chain


@tool(parse_docstring=True)
def risk_assessment_tool(location: str, activity: str, n_min: int = 7):
    """Create a risk assessment for a given location and activity.

    Args:
        location: Detailed description of where the activity will take place.
        activity: Detailed description of the activity.
        n_min: Minimum number of risks to identify.

    Returns:
        Risk assessment.
    """
    assessment_chain = build_assessment_chain()

    return assessment_chain.invoke(
        {
            "location": location,
            "activity": activity,
            "n_min": n_min,
        }
    )
