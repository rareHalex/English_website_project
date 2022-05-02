from flask import Flask, redirect, request, session
from flask import render_template
from searcher import training_tasks, find_content
import data_download
import sqlite3

app = Flask(__name__, static_folder='static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['POST', 'GET'])
@app.route('/main', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        word = request.form['title']
        session['word'] = word
        return redirect('/post')
    else:
        return render_template('main.html')


@app.route('/post')
def post():
    word = str(session.get('word', None))
    data = find_content.get_content(word)
    video = find_content.get_video(data)
    definition = find_content.get_definition(word)
    return render_template('post.html', articles=video,definition=definition)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/task')
def task():
    word = str(session.get('word', None))
    correct_word_problem = training_tasks.correct_word_task(word)
    correct_sentence_problem = training_tasks.build_correct_sentence_task(word)
    return render_template('task.html', frist_problem=correct_word_problem, second_problem=correct_sentence_problem)

if __name__ == '__main__':
    app.run()
    data_download.con.close()
    
    
