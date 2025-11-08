import random
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from custom_account.models import PasswordChangeOTP, UserModel


OTP_EXP_MINUTES = getattr(settings, 'PASSWORD_CHANGE_OTP_EXPIRE_MINUTES', 5)
OTP_RESEND_SECONDS = getattr(settings, 'PASSWORD_CHANGE_OTP_RESEND_SECONDS', 60)
OTP_MAX_ATTEMPTS = getattr(settings, 'PASSWORD_CHANGE_OTP_MAX_ATTEMPTS', 5)


class OTPThrottleError(Exception):
    """Raised when user requests OTP too frequently."""


class OTPExpiredError(Exception):
    pass


class OTPInvalidError(Exception):
    pass


class OTPAttemptsExceededError(Exception):
    pass


class OTPNotFoundError(Exception):
    pass


def _generate_code() -> str:
    return f"{random.randint(0, 999999):06d}"


def request_password_change_otp(user: UserModel) -> None:
    now = timezone.now()
    existing = PasswordChangeOTP.objects.filter(user=user, is_used=False).order_by('-created_at').first()
    if existing and not existing.is_expired and (now - existing.created_at).total_seconds() < OTP_RESEND_SECONDS:
        raise OTPThrottleError("OTP recently sent. Please wait before requesting again.")

    code = _generate_code()
    PasswordChangeOTP.objects.create(
        user=user,
        code_hash=make_password(code),
        expires_at=now + timedelta(minutes=OTP_EXP_MINUTES),
    )

    subject = "Mã OTP đổi mật khẩu"
    message = (
        f"Xin chào {user.username or user.email},\n\n"
        f"Mã OTP để đổi mật khẩu của bạn là: {code}.\n"
        f"Mã sẽ hết hạn sau {OTP_EXP_MINUTES} phút.\n\n"
        "Vui lòng không chia sẻ mã này cho bất kỳ ai."
    )
    default_sender = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
    send_mail(subject, message, default_sender, [user.email], fail_silently=False)


def verify_password_change_otp(user: UserModel, code: str) -> PasswordChangeOTP:
    now = timezone.now()
    otp = PasswordChangeOTP.objects.filter(user=user, is_used=False).order_by('-created_at').first()
    if not otp:
        raise OTPNotFoundError("Không tìm thấy OTP. Vui lòng yêu cầu mã mới.")

    if otp.is_expired:
        otp.is_used = True
        otp.save(update_fields=['is_used'])
        raise OTPExpiredError("OTP đã hết hạn. Vui lòng yêu cầu mã mới.")

    if otp.attempts >= OTP_MAX_ATTEMPTS:
        otp.is_used = True
        otp.save(update_fields=['is_used'])
        raise OTPAttemptsExceededError("Bạn đã nhập sai OTP quá số lần cho phép.")

    if not check_password(code, otp.code_hash):
        otp.attempts += 1
        otp.save(update_fields=['attempts'])
        raise OTPInvalidError("OTP không chính xác.")

    otp.is_used = True
    otp.save(update_fields=['is_used'])
    return otp
