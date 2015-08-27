__author__ = 'amin'

from django import forms
import models
from mysite.settings import NORECAPTCHA_SECRET_KEY

import urllib, urllib2
import re


class SignupForm():
    def __init__(self, data):
        self.username = data['username']
        self.email    = data['email']
        self.password = data['password']
        self.confpass = data['confpass']
        self.captcha  = ''#data['g-recaptcha-response']

    @staticmethod
    def username_errors(username):
        if not username:
            return 'username is empty'

        permitted_chars = ['.', '_']
        if username[0] in permitted_chars or username[-1] in permitted_chars:
            return 'username cannot begin or end with \'' + '\', \''.join(permitted_chars) + '\''

        for c in username:
            if not ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9') or (c in permitted_chars)):
                return 'username may only contain a-z A-Z 0-9 and \'' + '\', \''.join(permitted_chars) + '\'' + 'characters'

        if models.User.exists_user(username):
            return 'username already exists'

        return ''

    @staticmethod
    def email_errors(email):
        if not email:
            return 'email is empty'

        pattern = "\\b^((\w+[.|\w])*@(\w+[.])*\w+)\\b"
        if not re.findall(pattern, email):
            return 'email is invalid'

        return ''

    @staticmethod
    def password_errors(password):
        if not password:
            return 'password is empty'

        if len(password) < 5:
            return 'minimum length of password is 5 characters'

        numbers = [str(i) for i in range(10)]
        letters = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]

        def exists_char(lst):
            for l in lst:
                if l in password:
                   return True
            return False

        if not exists_char(numbers):
            return 'password needs at least one number'

        if not exists_char(letters):
            return 'password needs at least one letter'

        return ''

    @staticmethod
    def confpass_errors(_pass, conf):
        if not conf:
            return 'config password is empty'

        if not _pass == conf:
            return 'passwords does not match'
        return ''


    @staticmethod
    def captcha_errors(captcha):
        return ''
        if not captcha:
            return 'wrong captcha'

        post_data = {'secret': NORECAPTCHA_SECRET_KEY, 'response': captcha}
        result = urllib2.urlopen('https://www.google.com/recaptcha/api/siteverify', urllib.urlencode(post_data))
        resp = str(result.read())
        if not 'true' in resp:
            return 'wrong captcha'

        return ''

    def is_valid(self):
        if not self.username_errors(self.username) and  \
                not self.email_errors(self.email) and \
                not self.password_errors(self.password) and \
                not self.confpass_errors(self.password, self.confpass) and \
                not self.captcha_errors(self.captcha):
            return True
        return False


class LoginForm(forms.ModelForm):
    username = forms.CharField(label="username", max_length=32)
    password = forms.CharField(label="password", max_length=32)
