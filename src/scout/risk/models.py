from typing import Literal
from pydantic import BaseModel, Field
import uuid

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class Risk(BaseModel):
    """Describes a risk."""

    hazard: str = Field(
        description=(
            "Descriptions of the hazard. "
            "A hazard is something that may cause harm or damage."
        )
    )
    risks: list[str] = Field(
        description=(
            "Risks associated with the hazard. "
            "A risk is the harm that may occur from the hazard. "
            "Describe each risk in a sentence."
        )
    )
    affects: list[Literal["Young people", "Adult volunteers"]] = Field(
        description="Who is at risk."
    )
    controls: list[str] = Field(
        description=(
            "Controls are ways of making the activity safer by removing or reducing the "
            "risk. For example, you may use a different piece of equipment or you might "
            "change the way you do the activity."
        )
    )

    def to_markdown(self) -> str:
        # TODO can this be done in the pydantic Config class?
        return "\n".join(
            [
                "### Hazard",
                f"{self.hazard}",
                "### Affects",
                "\n\n".join([a for a in self.affects]),
                "### Risks",
                "\n\n".join([r for r in self.risks]),
                "### Controls",
                "\n\n".join([c for c in self.controls]),
                "\n\n",
            ]
        )


class RiskAssessment(BaseModel):
    """Risk assessment. Activity and location must be limited to a few words."""

    activity: str = Field(description="The activity.")
    location: str = Field(description="The location.")
    risks: list[Risk]

    def to_markdown(self) -> str:
        # TODO can this be done in the pydantic Config class?
        return "\n\n".join(
            [
                f"## {self.activity} - {self.location}",
                "\n\n".join([r.to_markdown() for r in self.risks]),
            ]
        )


class RiskAssessmentHumanInput(BaseModel):
    """Captures user input into the risk assessment."""

    activity: str = Field(description="Description of the activity.")
    location: str = Field(description="Description of the location.")
    n_min: int = Field(description="Minimum number of risks to return.")


class ExampleRiskAssessment(BaseModel):
    """Used to load examples from JSON."""

    input: RiskAssessmentHumanInput
    output: RiskAssessment

    def to_messages(
        self,
        human_message_template: str,
    ) -> tuple[HumanMessage, AIMessage, ToolMessage]:

        uid = str(uuid.uuid4())
        human = HumanMessage(human_message_template.format(**self.input.model_dump()))
        ai = AIMessage(
            content="",
            name=uid,
            tool_calls=[
                {
                    "name": self.output.model_json_schema()["title"],
                    "args": self.output.model_dump(),
                    "id": uid,
                }
            ],
        )
        tool = ToolMessage("", tool_call_id=uid)

        return (human, ai, tool)
