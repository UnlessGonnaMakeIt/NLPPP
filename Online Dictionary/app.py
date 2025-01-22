from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from models import db, Dictionary
import os
import pandas as pd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///replit.db')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')


db.init_app(app)


@app.before_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    person_entries = Dictionary.query.filter_by(category='person').order_by(Dictionary.english.asc()).all()
    place_entries = Dictionary.query.filter_by(category='place').order_by(Dictionary.english.asc()).all()
    proper_entries = Dictionary.query.filter_by(category='proper').order_by(Dictionary.english.asc()).all()
    return render_template('index.html', person_entries=person_entries, place_entries=place_entries, proper_entries=proper_entries)


@app.route('/add', methods=['POST'])
def add():
    category = request.form['category']
    english = request.form['english']
    chinese = request.form['chinese']
    new_entry = Dictionary(english=english, chinese=chinese, category=category)
    db.session.add(new_entry)
    db.session.commit()
    flash('Entry added successfully!')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    entry = Dictionary.query.get_or_404(id)
    if request.method == 'POST':
        entry.english = request.form['english']
        entry.chinese = request.form['chinese']
        db.session.commit()
        flash('Entry updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry)


@app.route('/delete/<int:id>')
def delete(id):
    entry = Dictionary.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted successfully!')
    return redirect(url_for('index'))


@app.route('/update-data', methods=['POST'])
def update_data():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        category = request.form.get('category')
        load_data(file_path, category)
        db.session.commit()
        flash('Data updated successfully!')
    return redirect(url_for('index'))


def load_data(file_path, category):
    """加载和保存数据到数据库"""
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        entry = Dictionary.query.filter_by(english=row['英文原词']).first()
        if entry:
            entry.chinese = row['中文译词']
            entry.category = category
        else:
            new_entry = Dictionary(english=row['英文原词'], chinese=row['中文译词'], category=category)
            db.session.add(new_entry)


@app.route('/download')
def download():
    person_entries = Dictionary.query.filter_by(category='person').all()
    place_entries = Dictionary.query.filter_by(category='place').all()
    proper_entries = Dictionary.query.filter_by(category='proper').all()
    # 分别创建不同类别的 DataFrame
    df_person = pd.DataFrame([(entry.english, entry.chinese, 'person') for entry in person_entries], columns=['English', 'Chinese', 'Category'])
    df_place = pd.DataFrame([(entry.english, entry.chinese, 'place') for entry in place_entries], columns=['English', 'Chinese', 'Category'])
    df_proper = pd.DataFrame([(entry.english, entry.chinese, 'proper') for entry in proper_entries], columns=['English', 'Chinese', 'Category'])
    # 合并不同类别的 DataFrame
    df = pd.concat([df_person, df_place, df_proper], ignore_index=True)
    excel_path = os.path.join(app.root_path, 'uploads', 'dictionary.xlsx')
    df.to_excel(excel_path, index=False)
    return send_file(excel_path, as_attachment=True, download_name='dictionary.xlsx')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)