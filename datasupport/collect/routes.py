#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-08-01
# @Update  : 2019-10-30
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @File    : routes.py
# @Desc    : 路由分发

import os
from collect import app, db
from config import Config
from collect.models import User, Analyze
from collect.forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, request, flash, redirect, url_for
from flask import send_from_directory
from pypinyin import pinyin, lazy_pinyin
from google_sheets import GoogleSheets
import google_sheets2
from hr_data import HrGoogleSheets
from email_attach import DownEmail


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', tiele='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename) + ' uploads success.'


@app.route('/uploads', methods=['POST', 'GET'])
def uploads():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('uploads.html')


@app.route('/manage_file')
def manage_file():
    files_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('manage_file.html', files_list=files_list)


@app.route('/open/<filename>')
def open_file(filename):
    file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template('browser.html', file_url=file_url)


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)
    return redirect(url_for('manage_file'))


@app.route('/googlesheets', methods=['POST', 'GET'])
def googlesheets():
    """
    IT数据支持，自动采集MOCK的表，处理后自动填入GoogleSheets的按索引取的表中
    :return:
    """
    if request.method == 'POST':
        if 'file' not in request.files or 'file2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        file2 = request.files['file2']
        if file.filename == '' or file2.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if request.form['sheet_num'] == '':
            flash('No selected sheet num')
            return redirect(request.url)
        if file and file2 and allowed_file(file.filename) and allowed_file(file2.filename):
            filename = "".join(lazy_pinyin(file.filename))
            filename = secure_filename(filename)
            file2_name = "".join(lazy_pinyin(file2.filename))
            file2_name = secure_filename(file2_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], file2_name))
            tables_name = request.form['tables_name']
            sheet_num = request.form['sheet_num']
            hr_googlesheets = GoogleSheets(filename=filename, file2_name=file2_name, tables_name=tables_name,
                                           sheet_num=sheet_num)
            result = hr_googlesheets.update()
            flash(result)
            return redirect(request.url)
    return render_template('googlesheets.html')


@app.route('/googlesheets2', methods=['POST', 'GET'])
def googlesheets2():
    """
    IT数据支持，自动采集MOCK的表，处理后自动填入GoogleSheets的相应表名中
    :return:
    """
    if request.method == 'POST':
        if 'file' not in request.files or 'file2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        file2 = request.files['file2']
        if file.filename == '' or file2.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if request.form['sheet_name'] == '':
            flash('No selected sheet name')
            return redirect(request.url)
        if file and file2 and allowed_file(file.filename) and allowed_file(file2.filename):
            filename = "".join(lazy_pinyin(file.filename))
            filename = secure_filename(filename)
            file2_name = "".join(lazy_pinyin(file2.filename))
            file2_name = secure_filename(file2_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], file2_name))
            tables_name = request.form['tables_name']
            sheet_name = request.form['sheet_name']
            hr_googlesheets2 = google_sheets2.GoogleSheets(filename=filename, file2_name=file2_name,
                                                           tables_name=tables_name,
                                                           sheet_name=sheet_name)
            result = hr_googlesheets2.append()
            if type(result) == dict:
                data = Analyze(result=result)
                db.session.add(data)
                db.session.commit()
            flash(result)
            return redirect(request.url)
    return render_template('googlesheets2.html')


@app.route('/hr2googlesheets', methods=['POST', 'GET'])
def hr2googlesheets():
    """
    IT数据支持，自动采集HR相关数据MOCK的表，处理后自动填入GoogleSheets的相应表名中
    :return:
    """
    if request.method == 'POST':
        if 'data_xlsx' not in request.files:
            flash('NO file part')
            return redirect(request.url)
        if request.form['week_sheet_name'] == '':
            flash('NO sheet name')
            return redirect(request.url)
        data_xlsx = request.files['data_xlsx']
        if data_xlsx.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if allowed_file(data_xlsx.filename):
            data_filename = "".join(lazy_pinyin(data_xlsx.filename))
            data_filename = secure_filename(data_filename)
            data_xlsx.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
            tables_name = request.form['tables_name']
            sheet_name = request.form["week_sheet_name"]
            hr_week = HrGoogleSheets(tables_name)
            result = hr_week.append_weekly(data_filename, sheet_name=sheet_name)
            if type(result) == dict:
                data = Analyze(result=result)
                db.session.add(data)
                db.session.commit()
            flash(result)
            return redirect(request.url)
    return render_template('hr2googlesheets.html')


@app.route('/hr_month2googlesheets', methods=['POST', 'GET'])
def hr_month2googlesheets():
    """
    IT数据支持，自动采集HR相关数据MOCK的表，处理后自动填入GoogleSheets的相应表名中
    :return:
    """
    if request.method == 'POST':
        if 'data_xlsx' not in request.files or 'pass_xlsx' not in request.files:
            flash('NO file part')
            return redirect(request.url)
        if request.form['month_sheet_name'] == '':
            flash('NO sheet name')
            return redirect(request.url)
        data_xlsx = request.files['data_xlsx']
        pass_xlsx = request.files['pass_xlsx']
        if data_xlsx.filename == '' or pass_xlsx.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if allowed_file(data_xlsx.filename) and allowed_file(pass_xlsx.filename):
            data_filename = "".join(lazy_pinyin(data_xlsx.filename))
            data_filename = secure_filename(data_filename)
            pass_filename = "".join(lazy_pinyin(pass_xlsx.filename))
            pass_filename = secure_filename(pass_filename)
            data_xlsx.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
            pass_xlsx.save(os.path.join(app.config['UPLOAD_FOLDER'], pass_filename))
            tables_name = request.form['tables_name']
            sheet_name = request.form["month_sheet_name"]
            hr_month = HrGoogleSheets(tables_name)
            result = hr_month.append_monthly(data_filename, pass_filename, sheet_name=sheet_name)
            if type(result) == dict:
                data = Analyze(result=result)
                db.session.add(data)
                db.session.commit()
            flash(result)
            return redirect(request.url)
    return render_template('hr_month2googlesheets.html')
