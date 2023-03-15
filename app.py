import openai
from flask import Flask, render_template, request, url_for, flash, redirect, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

messages = [{"role": "system", "content": "you are a helpful assistant that only speaks in Shakespearean English"},]

@app.route('/',  methods=('GET', 'POST'))
def index():
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

    return render_template('index.html', messages=messages)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if not session.get("key"):
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form['submit_button'] == "Clear":
            messages.clear()
            session["key"] = None
            return redirect(url_for('index'))
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
            return render_template('create.html', messages=messages[1:])

    return render_template('create.html')
