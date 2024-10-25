from langchain_core.prompts import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    MessagesPlaceholder,
                                    SystemMessagePromptTemplate)

system_prompt = """
A scout leader planning an activity for Scouts (aged 7-14) needs to perform a
risk assessment for an activity at a given location.

Your task is to perform a risk assessment identifying hazards and the risks
associated with them.

When identifying hazards and risks, please pay careful attention to the location
as this can introduce additional hazards.

Always consider the risks associated with poor or disruptive behaviour of
young people.

The following checklist is a good place to start when thinking about risks:

- Make sure everyone understands boundaries, limits and rules.
- Make sure games are suitable for age and ability of participants.
- Monitor behaviour of young people to make sure it remains suitable for the activity.
- Keep equipment in good order.
- Store chairs and tables safely.
- Reduce tripping or slipping hazards.
- Minimise potential for falls on solid or sharp objects and glass.
- Have a plan for what to do in an emergency.
- Have a first aid kit and trained first aider available.
- Have a procedure in place in case a child becomes separated from the group.
- Identify natural hazards in the area including water.
- Control fire risks.
- Have adequate ventilation from hazards of carbon monoxide.
- Make sure heating arrangements including boilers are safe.
- Make sure cooking arrangements are safe and hygienic.
- Visually inspect electrics - no bare wires or overloaded sockets.

Use plain British english and commonly used terms in your response.

Your tone should be formal.
"""

user_prompt = """
Location: {location}

Activity: {activity}

Identify {n_min} or more risk(s).
"""

assessment_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt),
        MessagesPlaceholder(variable_name="examples"),
        HumanMessagePromptTemplate.from_template(user_prompt),
    ]
)
