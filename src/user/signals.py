from django.dispatch import Signal

# plain_password contains original user password. It can be useful for some purposes (e.g. sending email
# with verification etc.)
user_registered = Signal(providing_args=['user', 'plain_password'])

user_email_confirmed = Signal(providing_args=['user', 'code'])

user_password_recovery_requested = Signal(providing_args=['request', 'email', 'is_valid'])
user_password_recovery_confirmed = Signal(providing_args=['request', 'code', 'is_valid'])
