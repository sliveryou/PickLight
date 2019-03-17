# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from . import web
from flask import render_template, redirect, url_for, current_app, flash
from flask_login import login_required, current_user


@web.route('/my/notes', methods=['GET', 'POST'])
@login_required
def my_note():
    return render_template('web/my_notes.html')
