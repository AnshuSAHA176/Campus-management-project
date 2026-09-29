from django.urls import path
from .views import AgentView,DocumentView


urlpatterns=[
    path('',AgentView.as_view(),name='campus agent'),
    path('knowledge/',DocumentView.as_view(),name='upload knowlage')
]
