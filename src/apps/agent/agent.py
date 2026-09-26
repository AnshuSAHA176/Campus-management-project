from langgraph.graph import StateGraph, START, END, add_messages
from pydantic import BaseModel
from typing import Annotated
from .tools import Tools
from .llm import get_model
from langgraph.prebuilt import ToolNode,tools_condition

def get_agent(access_token):
    model = get_model()

    class State(BaseModel):
        messages: Annotated[list, add_messages]

        domain: str | None = None

    graph_builder = StateGraph(State)

    get_today_schedule = Tools(access_token)
    tools = [
        get_today_schedule
    ]
    model_with_tool = model.bind_tools(tools)

    def agent(state:State):

        return {"messages":[model_with_tool.invoke(state.messages)]}

    graph_builder.add_node('agent',agent)
    graph_builder.add_node('tools',ToolNode(tools))

    graph_builder.add_edge(START,'agent')
    graph_builder.add_conditional_edges('agent',tools_condition)
    graph_builder.add_edge('tools','agent')

    return graph_builder.compile()