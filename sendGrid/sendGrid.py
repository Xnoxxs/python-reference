from pathlib import Path

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config.variables import MyVariables


class MySendGrid:

    @staticmethod
    def send_email(recipient: str):
        """
        Send an email with the given designs and repositories.

        :param recipient: str → recipient email
        :param html_file: str → file name inside SendGrid/Designs (e.g., "owner_new_booking.html")
        :param email_data: dict → repositories for the Jinja2 designs
        """

        # Debug: Check if API key is loaded
        api_key = MyVariables.sendgrid_api_key

        result_path = Path(__file__).parent / "Template" / "result.html"

        message = Mail(
            from_email='test@adenvo.com',
            to_emails=recipient,
            subject='Hello from Adnevo',
            html_content=result_path.read_text(encoding="utf-8")
        )

        try:
            sg = SendGridAPIClient(api_key)
            sg.send(message)

            print(f"✅ Email sent to {recipient}")

        except Exception as e:
            print(f"❌ Send Email Error: {e}")



