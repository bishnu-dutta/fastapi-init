from fastapi_mail import MessageSchema, MessageType


def create_email_message(subject :str, recipients:list[str], body:str):

    message = MessageSchema(
        subject = subject,
        recipients = recipients,
        body=body,
        subtype = MessageType.html
    )
    return message




