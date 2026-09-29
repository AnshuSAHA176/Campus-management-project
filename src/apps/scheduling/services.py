import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from config import settings


def send_email(to_email,name , subject, html_content):

     configuration = sib_api_v3_sdk.Configuration()
     configuration.api_key["api-key"] = settings.BREVO_API_KEY
 
     api_client = sib_api_v3_sdk.ApiClient(configuration)
     api = sib_api_v3_sdk.TransactionalEmailsApi(api_client)
 
     
 
     
     email_data = sib_api_v3_sdk.SendSmtpEmail(
             sender={
                 "name": settings.BREVO_SENDER_NAME,
                 "email": settings.BREVO_SENDER_EMAIL,
             },
             to=[
                 {
                     "email": to_email,
                     "name": name,
                 }
             ],
             subject=subject,
             html_content=html_content,
         )
 
     try:
 
        response = api.send_transac_email(email_data)
 
        print(
                 f"Email sent to {to_email}: {response}"
             )
 
     except ApiException as e:
 
        print(
                 f"Brevo email failed for {to_email}: {e}"
             )
 
     return "notifications sent"