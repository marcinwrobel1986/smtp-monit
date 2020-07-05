from email.message import EmailMessage

from aiosmtplib import SMTP

from config.config import Config


class SmtpSender:
    def __init__(self):
        self.config = Config()
        self.hostname = self.config.get_email_config().get('hostname', '')
        self.port = self.config.get_email_config().get('port', '')
        self.use_tls = self.config.get_email_config().get('use_tls', '')
        self.username = self.config.get_email_config().get('username', '')
        self.password = self.config.get_email_config().get('password', '')
        self.smtp_client = SMTP(hostname=self.hostname, port=self.port, use_tls=self.use_tls, username=self.username,
                                password=self.password)

    def get_msg(self, subject: str, content: str) -> EmailMessage:
        message = EmailMessage()
        message["From"] = self.config.get_email_config().get('from', '')
        message["To"] = self.config.get_email_config().get('to', '')
        message["Subject"] = subject
        message.set_content(content)
        return message

    async def send_message(self, subject: str, content: str) -> None:
        message = self.get_msg(subject=subject, content=content)
        async with self.smtp_client:
            await self.smtp_client.send_message(message)
