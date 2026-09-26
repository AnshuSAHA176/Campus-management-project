from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from .agent import get_agent

from rest_framework.response import Response

from langchain.messages import SystemMessage,HumanMessage

system_message = """
You are CivicAI, a campus complaint assistant.

Tool usage rules:

- Use get_similar_complaints when the user asks to find similar
  or duplicate complaints.
- The result of get_similar_complaints already contains the required
  information: complaint ID, complaint title, and similarity score.
- After calling get_similar_complaints, return those results directly.
- DO NOT call get_complaint_details for the returned complaints unless
  the user explicitly asks for details about one of them.
- Use get_complaint_details only when the user explicitly requests
  information about a specific complaint.
"""


class AgentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        access_token = self._get_token(request)

        agent = get_agent(access_token=access_token)

        response = agent.invoke(
            SystemMessage(content=system_message),
            HumanMessage(content=request.data.get('message',''))

            
                )
        return Response({"content":response["messages"][-1].content})
        

    def _get_token(self, request):
        auth_header = request.headers.get("Authorization", "")
        return auth_header.replace("Bearer ", "")
