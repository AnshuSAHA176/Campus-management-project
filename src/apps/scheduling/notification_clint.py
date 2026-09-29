from celery import shared_task

from config import settings

import sib_api_v3_sdk

from sib_api_v3_sdk.rest import ApiException

from .models import ClassSession
from .services import send_email

@shared_task(bind=True, ignore_result=True)
def wanotification(self, instance_id):

    class_session = (
        ClassSession.objects
        .select_related(
            "batch",
            "subject",
            "teacher",
            "room",
        )
        .filter(id=instance_id)
        .first()
    )

    if not class_session:
        return "class no longer exists"
    
    # Create Brevo client once
    
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY

    api_client = sib_api_v3_sdk.ApiClient(configuration)
    api = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

    students = (
        class_session.batch.students
        .select_related("user")
        .all()
    )

    for student in students:

        email = student.user.email

        if not email:
            continue
        HTML_CONTENT = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Class Scheduled</title>
</head>

<body style="
    margin: 0;
    padding: 0;
    background-color: #f4f5f7;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    color: #101828;
">

    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f5f7; padding: 40px 15px;">
        <tr>
            <td align="center">

                <!-- Main Email Container -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="
                    max-width: 560px;
                    background-color: #ffffff;
                    border: 1px solid #e4e7ec;
                    border-radius: 4px;
                    overflow: hidden;
                ">

                    <!-- Header -->
                    <tr>
                        <td style="
                            padding: 32px 40px;
                            background-color: #0c111d;
                            color: #ffffff;
                        ">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td>
                                        <div style="
                                            font-size: 11px;
                                            font-weight: 600;
                                            letter-spacing: 0.8px;
                                            text-transform: uppercase;
                                            color: #94a3b8;
                                            margin-bottom: 8px;
                                        ">
                                            Campus Management
                                        </div>
                                        <div style="
                                            font-size: 24px;
                                            font-weight: 600;
                                            line-height: 1.3;
                                            color: #ffffff;
                                        ">
                                            New Class Scheduled
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Body Content -->
                    <tr>
                        <td style="padding: 40px;">

                            <p style="
                                margin: 0 0 12px;
                                font-size: 15px;
                                color: #101828;
                            ">
                                Dear <strong>{student.full_name}</strong>,
                            </p>

                            <p style="
                                margin: 0 0 32px;
                                font-size: 15px;
                                line-height: 1.6;
                                color: #475467;
                            ">
                                A new class session has been confirmed for your batch. Please find the official schedule details below.
                            </p>

                            <!-- Clean, Ticket-Style Details Table -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="
                                border-top: 1px solid #eaecf0;
                            ">
                                
                                <tr>
                                    <td style="padding: 14px 0; border-bottom: 1px solid #eaecf0; width: 35%; font-size: 13px; font-weight: 600; color: #475467;">
                                        Subject
                                    </td>
                                    <td align="right" style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 14px; font-weight: 500; color: #101828;">
                                        {class_session.subject.name}
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 13px; font-weight: 600; color: #475467;">
                                        Instructor
                                    </td>
                                    <td align="right" style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 14px; color: #101828;">
                                        {class_session.teacher.full_name}
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 13px; font-weight: 600; color: #475467;">
                                        Date
                                    </td>
                                    <td align="right" style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 14px; font-weight: 500; color: #101828;">
                                        {class_session.date}
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 13px; font-weight: 600; color: #475467;">
                                        Time
                                    </td>
                                    <td align="right" style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 14px; font-weight: 500; color: #101828;">
                                        {class_session.start_time} &ndash; {class_session.end_time}
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 13px; font-weight: 600; color: #475467;">
                                        Room / Location
                                    </td>
                                    <td align="right" style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 14px; color: #101828;">
                                        {class_session.room.room_number}
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 13px; font-weight: 600; color: #475467;">
                                        Batch Assigned
                                    </td>
                                    <td align="right" style="padding: 14px 0; border-bottom: 1px solid #eaecf0; font-size: 14px; color: #101828;">
                                        {class_session.batch.name}
                                    </td>
                                </tr>
                            </table>

                            <!-- Professional Notice Box -->
                            <div style="
                                margin-top: 32px;
                                padding: 16px 20px;
                                background-color: #f8f9fa;
                                border: 1px solid #eaecf0;
                                border-radius: 4px;
                            ">
                                <p style="
                                    margin: 0;
                                    font-size: 13px;
                                    line-height: 1.6;
                                    color: #475467;
                                ">
                                    <strong style="color: #344054;">Attendance Notice:</strong> Please ensure you arrive promptly at the scheduled time. If you have a scheduling conflict, contact your department administrator immediately.
                                </p>
                            </div>

                            <p style="
                                margin: 32px 0 0;
                                font-size: 14px;
                                line-height: 1.6;
                                color: #475467;
                            ">
                                Sincerely,<br>
                                <strong style="color: #101828;">Campus Administration</strong>
                            </p>

                        </td>
                    </tr>

                    <!-- Minimalist Footer -->
                    <tr>
                        <td style="
                            padding: 24px 40px;
                            background-color: #fcfcfd;
                            border-top: 1px solid #eaecf0;
                            text-align: left;
                        ">
                            <p style="
                                margin: 0 0 8px;
                                font-size: 12px;
                                line-height: 1.5;
                                color: #98a2b3;
                            ">
                                This is an automated system notification generated by Campus Management. Please do not reply directly to this email.
                            </p>
                            <p style="
                                margin: 0;
                                font-size: 12px;
                                line-height: 1.5;
                                color: #98a2b3;
                            ">
                                &copy; 2024 Campus Management. All rights reserved.
                            </p>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""
        send_email(to_email=email,name=student.full_name,subject="New Class Scheduled",html_content=HTML_CONTENT)
       
    return "notifications sent"


@shared_task(bind=True, ignore_result=True)
def beforeclass(self, instance_id):

    class_session = (
        ClassSession.objects
        .select_related(
            "teacher",
            "subject",
            "batch",
            "room",
        )
        .filter(id=instance_id)
        .first()
    )

    if not class_session:
        return "class no longer exists"

    if class_session.status != ClassSession.Status.SCHEDULED:
        return "class is no longer scheduled"

    subject = f"Class Reminder: {class_session.subject.name} starts in 15 minutes"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Class Reminder</title>
    </head>

    <body style="
        margin: 0;
        padding: 0;
        background-color: #f4f6f8;
        font-family: Arial, Helvetica, sans-serif;
        color: #1f2937;
    ">

        <table
            width="100%"
            cellpadding="0"
            cellspacing="0"
            style="background-color: #f4f6f8; padding: 40px 16px;"
        >
            <tr>
                <td align="center">

                    <table
                        width="100%"
                        cellpadding="0"
                        cellspacing="0"
                        style="
                            max-width: 600px;
                            background-color: #ffffff;
                            border: 1px solid #e5e7eb;
                            border-radius: 12px;
                            overflow: hidden;
                        "
                    >

                        <!-- Header -->
                        <tr>
                            <td style="
                                padding: 28px 32px;
                                background-color: #2563eb;
                                color: #ffffff;
                            ">
                                <div style="
                                    font-size: 14px;
                                    font-weight: 600;
                                    letter-spacing: 0.5px;
                                    margin-bottom: 8px;
                                ">
                                    CAMPUS MANAGEMENT
                                </div>

                                <div style="
                                    font-size: 25px;
                                    font-weight: 700;
                                ">
                                    Class Reminder
                                </div>
                            </td>
                        </tr>

                        <!-- Content -->
                        <tr>
                            <td style="padding: 32px;">

                                <p style="
                                    margin: 0 0 16px;
                                    font-size: 16px;
                                    line-height: 1.6;
                                ">
                                    Hello
                                    <strong>
                                        {class_session.teacher.full_name}
                                    </strong>,
                                </p>

                                <p style="
                                    margin: 0 0 24px;
                                    font-size: 15px;
                                    line-height: 1.7;
                                    color: #4b5563;
                                ">
                                    This is a reminder that your class
                                    starts in approximately
                                    <strong>15 minutes</strong>.
                                </p>

                                <!-- Class details -->
                                <table
                                    width="100%"
                                    cellpadding="0"
                                    cellspacing="0"
                                    style="
                                        border: 1px solid #e5e7eb;
                                        border-radius: 8px;
                                        overflow: hidden;
                                    "
                                >

                                    <tr>
                                        <td style="
                                            padding: 14px 16px;
                                            background-color: #f9fafb;
                                            font-size: 14px;
                                            font-weight: 600;
                                            color: #6b7280;
                                            width: 35%;
                                        ">
                                            Subject
                                        </td>

                                        <td style="
                                            padding: 14px 16px;
                                            font-size: 14px;
                                            font-weight: 600;
                                            color: #111827;
                                        ">
                                            {class_session.subject.name}
                                        </td>
                                    </tr>

                                    <tr>
                                        <td style="
                                            padding: 14px 16px;
                                            background-color: #f9fafb;
                                            font-size: 14px;
                                            font-weight: 600;
                                            color: #6b7280;
                                        ">
                                            Batch
                                        </td>

                                        <td style="
                                            padding: 14px 16px;
                                            font-size: 14px;
                                            color: #111827;
                                        ">
                                            {class_session.batch.name}
                                        </td>
                                    </tr>

                                    <tr>
                                        <td style="
                                            padding: 14px 16px;
                                            background-color: #f9fafb;
                                            font-size: 14px;
                                            font-weight: 600;
                                            color: #6b7280;
                                        ">
                                            Date
                                        </td>

                                        <td style="
                                            padding: 14px 16px;
                                            font-size: 14px;
                                            color: #111827;
                                        ">
                                            {class_session.date}
                                        </td>
                                    </tr>

                                    <tr>
                                        <td style="
                                            padding: 14px 16px;
                                            background-color: #f9fafb;
                                            font-size: 14px;
                                            font-weight: 600;
                                            color: #6b7280;
                                        ">
                                            Time
                                        </td>

                                        <td style="
                                            padding: 14px 16px;
                                            font-size: 14px;
                                            color: #111827;
                                        ">
                                            {class_session.start_time}
                                            &nbsp;&ndash;&nbsp;
                                            {class_session.end_time}
                                        </td>
                                    </tr>

                                    <tr>
                                        <td style="
                                            padding: 14px 16px;
                                            background-color: #f9fafb;
                                            font-size: 14px;
                                            font-weight: 600;
                                            color: #6b7280;
                                        ">
                                            Room
                                        </td>

                                        <td style="
                                            padding: 14px 16px;
                                            font-size: 14px;
                                            color: #111827;
                                        ">
                                            {class_session.room.room_number}
                                        </td>
                                    </tr>

                                </table>

                                <!-- Reminder -->
                                <div style="
                                    margin-top: 28px;
                                    padding: 16px;
                                    background-color: #eff6ff;
                                    border-left: 4px solid #2563eb;
                                ">
                                    <p style="
                                        margin: 0;
                                        font-size: 14px;
                                        line-height: 1.6;
                                        color: #374151;
                                    ">
                                        Please make your way to the classroom
                                        and be ready for the session.
                                    </p>
                                </div>

                                <p style="
                                    margin: 28px 0 0;
                                    font-size: 14px;
                                    line-height: 1.6;
                                    color: #6b7280;
                                ">
                                    Regards,<br>
                                    <strong style="color: #111827;">
                                        Campus Management
                                    </strong>
                                </p>

                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="
                                padding: 20px 32px;
                                background-color: #f9fafb;
                                border-top: 1px solid #e5e7eb;
                                text-align: center;
                            ">
                                <p style="
                                    margin: 0;
                                    font-size: 12px;
                                    color: #9ca3af;
                                ">
                                    This is an automated notification from
                                    Campus Management.
                                </p>
                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """

    send_email(
        to_email=class_session.teacher.user.email,
        subject=subject,
        html_content=html_content,
        name= class_session.teacher.full_name
    )

    return "done"



