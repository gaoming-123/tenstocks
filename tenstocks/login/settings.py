
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'gaomingjiang123@sina.com'
EMAIL_HOST_PASSWORD = 'gaomingjiang'

CONFIRM_DAYS = 7

SECRET_KEY='(t39gjj^-5ztj@i18m_lz1#p^t63juo%2#@#3f--ew1zu!mhyn'

EMAIL_USE_TLS = True # 这里必须是 True，否则发送不成功
EMAIL_FROM = 'gaomingjiang123@sina.com' # 你的 邮箱 账号
DEFAULT_FROM_EMAIL = 'gaomingjiang123@sina.com'
# ----------------