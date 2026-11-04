
from typing import Annotated
from pydantic import BaseModel
from langgraph.checkpoint.memory import InMemorySaver


CAMPUS_KEYWORDS = {
    "campus", "university", "college", "department",
    "student", "students", "teacher", "teachers",
    "professor", "batch", "subject", "classroom",
    "room", "schedule", "timetable", "class",
    "attendance", "exam", "examination", "admission",
    "curriculum", "course", "courses", "research",
    "regulation", "regulations", "policy", "policies",
    "notice", "document", "documents", "pdf",
    "knowledge", "academic",
}

checkpointer = InMemorySaver()


def get_agent(access_token):

    from langgraph.graph import StateGraph, START, END, add_messages
    from langgraph.prebuilt import ToolNode, tools_condition
    from langchain.messages import HumanMessage, AIMessage

    from .tools import Tools
    from .llm import get_model
    from .domain import domain_classifier

    model = get_model()

    class State(BaseModel):
        messages: Annotated[list, add_messages]
        domain: str | None = None

    graph_builder = StateGraph(State)

    tools = list(Tools(access_token))

    model_with_tool = model.bind_tools(tools)
    for index, tool in enumerate(tools):
        print({
            "index": index,
            "type": type(tool).__name__,
            "name": getattr(tool, "name", None),
            "args": getattr(tool, "args", None),
        })

        assert getattr(tool, "name", None), (
            f"Invalid tool at index {index}: {tool}"
        )
    async def domain_classifier_node(state: State):

        human_messages = [
            message
            for message in state.messages
            if isinstance(message, HumanMessage)
        ]

        conversation = "\n".join(
            message.content for message in human_messages[-3:]
        )

        text = conversation.lower()

        if any(keyword in text for keyword in CAMPUS_KEYWORDS):
            return {"domain": "campus"}

        domain = await domain_classifier(conversation)

        return {"domain": domain}

    def domain_router(state: State):
        return "offtopic" if state.domain != "campus" else "ontopic"

    def reject_topic(state: State):
        return {
            "messages": [
                AIMessage(
                    content=(
                        "I can help with your campus management system, "
                        "but I can't help with that topic."
                    )
                )
            ]
        }

    async def agent(state: State):
        response = await model_with_tool.ainvoke(state.messages[-3:])
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    async def execute_tools(state: State):
        return await tool_node.ainvoke(state)

    graph_builder.add_node("domain_classifier", domain_classifier_node)
    graph_builder.add_node("reject", reject_topic)
    graph_builder.add_node("agent", agent)
    graph_builder.add_node("tools", execute_tools)

    graph_builder.add_edge(START, "domain_classifier")

    graph_builder.add_conditional_edges(
        "domain_classifier",
        domain_router,
        {
            "offtopic": "reject",
            "ontopic": "agent",
        }
    )

    graph_builder.add_edge("reject", END)

    graph_builder.add_conditional_edges("agent", tools_condition)

    graph_builder.add_edge("tools", "agent")

    return graph_builder.compile(checkpointer=checkpointer)
