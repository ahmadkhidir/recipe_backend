from django.conf import settings
import pyotp
import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class OTP:
    _totp = pyotp.TOTP(settings.PYOTP_KEY, interval=settings.PYOTP_INTERVAL)

    @staticmethod
    def generate_otp() -> str:
        return OTP._totp.now()

    @staticmethod
    def verify_otp(token: str) -> bool:
        return OTP._totp.verify(token)


class Email:
    @staticmethod
    def send_email(subject, html_content, to: list):
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            to=to
        )
        email.attach_alternative(html_content, "text/html")
        EmailThread(email).start()

    @staticmethod
    def send_reset_otp(email, otp):
        subject = "Password Reset OTP"
        supportEmail = settings.SUPPORT_EMAIL
        companyName = settings.COMPANY_NAME
        html_content = render_to_string("utils/emails/reset_password.html", {
                                        "otp": otp, "supportEmail": supportEmail, "companyName": companyName, })
        Email.send_email(subject, html_content, [email])


ACCOUNT_TYPES = [('regular', 'Regular'), ('chef', 'Chef')]
INGREDIENT_MEASURES = [('g', 'Grams'), ('kg', 'Kilograms'), ('ml', 'Milliliters'), ('l', 'Liters'), ('tsp', 'Teaspoon'), (
    'tbsp', 'Tablespoon'), ('cup', 'Cup'), ('pint', 'Pint'), ('quart', 'Quart'), ('gallon', 'Gallon'), ('oz', 'Ounce'), ('lb', 'Pound')]
