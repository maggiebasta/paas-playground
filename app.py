import openai
from flask import Flask, render_template, request, url_for, flash, redirect, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/',  methods=('GET', 'POST'))
def index():
    session["messages"] = []
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Open AI Key is required!')
        else:
            try:
                openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "hi"}],
                    api_key=content,
                )
            except openai.error.AuthenticationError:
                flash('Invalid API key!')
            else:
                session["key"] = content
                return redirect(url_for('create'))

    return render_template('index.html', messages=session["messages"])


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if not session.get("key"):
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form['submit_button'] == "Clear":
            session["messages"] = []
            session["key"] = None
            return redirect(url_for('index'))
        content = request.form['content']
        if not content:
            flash('Content is required!')
                
        else:
            session["messages"].append({"role": "user",'content': content})
            system_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=session["messages"],
                api_key=session["key"],
            )
            session["messages"].append(
                {"role": "system", "content": system_response['choices'][0]['message']['content']}
            )
            return render_template('create.html', messages=session["messages"])

    return render_template('create.html')