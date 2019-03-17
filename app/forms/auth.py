# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from wtforms import Form, StringField, PasswordField, ValidationError
from wtforms.validators import Length, Email, DataRequired, EqualTo
from app.models.user import User
from flask_login import current_user


class EmailForm(Form):
    # 电子邮箱表单
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不可以为空，请输入你的邮箱'),
        Length(6, 64, message='邮箱长度至少需要在6到64个字符之间'),
        Email(message='电子邮箱不符合规范')])


class RegisterForm(EmailForm):
    # 注册表单
    nickname = StringField('昵称', validators=[
        DataRequired(message='昵称不可以为空，请输入你的昵称'),
        Length(2, 10, message='昵称至少需要2个字符，最多10个字符')])

    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'),
        Length(6, 20, message='密码长度至少需要在6到20个字符之间')])

    def validate_email(self, field):
        # 自定义验证器，验证电子邮箱是否已被注册
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')


class LoginForm(EmailForm):
    # 登录表单
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 20)])


class ResetPasswordForm(Form):
    # 重置密码表单
    password1 = PasswordField('新密码', validators=[
        DataRequired('新密码不可以为空，请输入新密码'),
        Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不一致')])

    password2 = PasswordField('确认新密码', validators=[
        DataRequired('确认密码不可以为空，请输入确认密码'), Length(6, 20)])


class ChangePasswordForm(Form):
    # 修改密码表单
    old_password = PasswordField('原密码', validators=[DataRequired('原密码不可以为空，请输入原密码')])

    new_password1 = PasswordField('新密码', validators=[
        DataRequired('新密码不可以为空，请输入新密码'),
        Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])

    new_password2 = PasswordField('新密码', validators=[DataRequired('确认密码不可以为空，请输入确认密码')])

    def validate_old_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('原密码校验失败')
