from langchain import tools
from .services import Services

BASE_URL = 'localhost:8000/'



def Tools(access_token):
    services = Services(base_url=BASE_URL,access_token=access_token)


    @tools
    def get_today_schedule():
        """
        Get today's scheduled classes for the current user.
        """
        return services.get_today_schedule()

    return get_today_schedule

