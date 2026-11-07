
from typing import Annotated
import re

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

    def get_conversation(messages, keep_messages=8):

        recent_messages = messages[-keep_messages:]
        conversation = []

        for message in recent_messages:

            if isinstance(message, HumanMessage):
                role = "User"

            elif isinstance(message, AIMessage):
                role = "Assistant"

            else:
                continue

            content = message.content

            if isinstance(content, str) and content.strip():
                conversation.append(f"{role}: {content}")

        return "\n".join(conversation)

    def contains_campus_keyword(message):

        text = message.lower()

        return any(
            re.search(rf"\b{re.escape(keyword)}\b", text)
            for keyword in CAMPUS_KEYWORDS
        )

    async def domain_classifier_node(state: State):

        human_messages = [
            message
            for message in state.messages
            if isinstance(message, HumanMessage)
        ]

        if not human_messages:
            return {"domain": "unknown"}

        current_message = human_messages[-1].content

        if not isinstance(current_message, str):
            current_message = str(current_message)

        if contains_campus_keyword(current_message):
            return {"domain": "campus"}

        conversation = get_conversation(state.messages)

        domain = await domain_classifier(conversation)

        return {"domain": domain}

    def domain_router(state: State):

        return (
            "ontopic"
            if state.domain == "campus"
            else "offtopic"
        )

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

    def window_messages(messages, keep_turns=3):

        human_indices = [
            i
            for i, message in enumerate(messages)
            if isinstance(message, HumanMessage)
        ]

        if not human_indices:
            return messages

        start = (
            human_indices[-keep_turns]
            if len(human_indices) >= keep_turns
            else human_indices[0]
        )

        return messages[start:]

    async def agent(state: State):

        response = await model_with_tool.ainvoke(
            window_messages(state.messages)
        )

        return {"messages": [response]}

    tool_node = ToolNode(tools)

    async def execute_tools(state: State):

        return await tool_node.ainvoke(state)

    graph_builder.add_node(
        "domain_classifier",
        domain_classifier_node
    )

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

    graph_builder.add_conditional_edges(
        "agent",
        tools_condition
    )

    graph_builder.add_edge("tools", "agent")

    return graph_builder.compile(
        checkpointer=checkpointer
    )
