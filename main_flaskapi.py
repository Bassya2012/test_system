import sys

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../functions')))

from functions.playdb import insert_data, names_tests, delete_select_data, delete_all_data, delete_all_result, \
    create_table_with_added_tests, create_table_with_tests_results, get_all_add_test_data, get_all_result_test_data, \
    get_path
from flask import Flask, render_template

app = Flask(__name__)

create_table_with_added_tests()
create_table_with_tests_results()

def path_for_task(path):
    path_rename = path.replace('\\', '/')
    substring = "/home"
    index = path_rename.find(substring)
    if index != -1:
        exact_path = path_rename[index:]
    else:
        exact_path = path_rename
    return exact_path

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/delete', methods=['POST'])
def delete():
    data = request.form['data']
    data = [int(x) for x in data.split(',')]
    print('data from form', data)
    for i in data:
        print('i is here', i)
        path = get_path(i)
        file_path = path[0]
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"файл '{file_path}' был успешно удален")
        else:
            print(f"файл '{file_path}' не существует")
        delete_select_data(i)
    return table_test()


@app.route('/deleteall', methods=['POST'])
def deleteall():
    delete_all_result()
    return render_template('index.html')


@app.route('/clean', methods=['POST'])
def clean():
    delete_all_data()
    return render_template('index.html', result='база данных очищена')


file_path = os.path.dirname(os.path.abspath(__file__))
path_for_dir = os.path.join(file_path, 'tests_for_system')
app.config['UPLOAD_FOLDER'] = path_for_dir

@app.route('/upload', methods=['POST'])
def upload_file():
    time = request.form['time']
    if time == '':
        time = '* * * * *'
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    file_name = file.filename
    p = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    print('path to file', p)
    path = path_for_task(p)
    if file_name != '':
        insert_data(file_name, time, path)
        names_tests()
    else:
        file_name = 'No file uploaded'
    return render_template('index.html', result=file_name)


@app.route('/table')
def show_table():
    data = get_all_result_test_data()
    return render_template('table.html', data=data)


@app.route('/table_test')
def table_test():
    data = get_all_add_test_data()
    return render_template('table_test.html', data=data)

@app.route('/delete_select',methods=['POST'])
def delete_select():
    data = get_all_add_test_data()
    return render_template('table_test.html', data=data)


if __name__ == '__main__':
    app.run()
