from django.core.mail import EmailMessage


def send_verify_mail(user):
    verify_link = f'{reverse("auth:verify")}?email={user.email}&activation_key={user.activation_key}'
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} используйте' \
        f'следующий код активации: \n<b>{user.activation_key}</b>\n или перейдите по ссылке:' \
        f'\n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)