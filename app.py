from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

# Temporary user storage (no database)
users = {}

tasks = []

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', tasks=tasks, user=session['user'])

# -------- AUTH -------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid Credentials ❌"

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users[username] = password
        return redirect('/login')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# -------- TASK -------- #

@app.route('/add', methods=['POST'])
def add():
    if 'user' in session:
        task = request.form.get('task')
        if task:
            tasks.append(task)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    if 'user' in session:
        tasks.pop(index)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)