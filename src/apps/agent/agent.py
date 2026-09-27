from langgraph.graph import StateGraph, START, END, add_messages
from pydantic import BaseModel
from typing import Annotated
from .tools import Tools
from .llm import get_model
from langgraph.prebuilt import ToolNode, tools_condition
from .domain import domain_classifier
from langchain.messages import HumanMessage, AIMessage


def get_agent(access_token):
    model = get_model()

    class State(BaseModel):
        messages: Annotated[list, add_messages]

        domain: str | None = None

    graph_builder = StateGraph(State)

    get_today_schedule,get_available_rooms = Tools(access_token)
    tools = [get_today_schedule,get_available_rooms]
    model_with_tool = model.bind_tools(tools)

    def domain_classifier_node(state: State):

        human_messages = [
            message for message in state.messages if message.type == "human"
        ]

        recent_human_messages = human_messages[-3:]

        conversation = "\n".join(message.content for message in recent_human_messages)

        domain = domain_classifier(conversation)

        return {"domain": domain}

    def domain_router(state: State):
        domain = state.domain
        if domain != "campus":
            return "offtopic"
        return "ontopic"

    def reject_topic(state: State):

        return {
            "messages": [
                AIMessage(
                    content="I can help with your campus management system, but I can't help "
                    "with that topic. Try asking me about schedules, timetables, "
                    "teachers, students, subjects, batches, rooms, or class scheduling."
                )
            ]
        }

    def agent(state: State):

        return {"messages": [model_with_tool.invoke(state.messages)]}

    graph_builder.add_node("domain_classifier", domain_classifier_node)

    graph_builder.add_node("reject", reject_topic)
    graph_builder.add_node("agent", agent)
    graph_builder.add_node("tools", ToolNode(tools))
    # edges

    graph_builder.add_edge(START, "domain_classifier")

    graph_builder.add_conditional_edges(
        "domain_classifier", domain_router, {"offtopic": "reject", "ontopic": "agent"}
    )

    graph_builder.add_edge("reject", END)
    graph_builder.add_conditional_edges("agent", tools_condition)
    graph_builder.add_edge("tools", "agent")

    return graph_builder.compile()
