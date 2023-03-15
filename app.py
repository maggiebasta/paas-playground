import openai
from flask import Flask, render_template, request, url_for, flash, redirect, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

messages = []

@app.route('/',  methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Open AI Key is required!')

        else:
            session["key"] = content
            return redirect(url_for('create'))

    return render_template('index.html', messages=messages)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if not session.get("key"):
        return redirect(url_for('index'))
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
                
        else:
            messages.append({"role": "user",'content': content})
            system_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                api_key=session["key"],
            )
            messages.append(
                {"role": "system", "content": system_response['choices'][0]['message']['content']}
            )
            return render_template('create.html', messages=messages)

    return render_template('create.html')