from flask import Flask, session, render_template, request, redirect, flash
from collections import namedtuple

import uuid

app = Flask(__name__)
app.secret_key = b'asdfjaksfjkljrkljadlkja'

messages = {}
loggedIn = False

Message = namedtuple('Message', 'text, likes')


@app.route('/')
def index():
    return render_template('view.html', messages=messages)

def show_messages(messages):
    return render_template('view.html', messages=messages)


@app.route('/message', methods=['POST'])
def handle_data():
	request.form['message']
	text = request.form['message']
	message =  Message(text, 0)
	if len(message.text) != 0 and len(message.text) < 140:
		messages[str(uuid.uuid4())] = message
		flash(u'Your message was posted', 'success')
	else:
		if len(message.text) == 0:
			flash('You must provide a message', 'danger')
		else:
			flash('Sorry, your message is to long, only 140 characters are allowed', 'danger')
	return show_messages(messages)


@app.route('/like/<uuid>')
def like(uuid):	
	message = messages[uuid]
	if message is not None:
		new_message = Message(message.text, message.likes + 1)
		messages[uuid] = new_message
	return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username == "admin" and password == "messageapp":
			session['authenticated'] = True		
			return redirect('/admin')
		else:
			flash(u'Invalid credentials provided', 'danger')
	return render_template('login.html')


@app.route('/logout')
def logout():
	session['authenticated'] = False
	flash(u'You are logged out', 'success')
	return redirect('/')


@app.route('/admin')
def admin_page():
	if is_admin():
		return render_template('admin.html', messages=messages)
	else:
		session['authenticated'] = False
		return redirect('/login')


#admin function
@app.route('/clear_messages')
def clear_messages():
	messages.clear()
	flash(u'All messages have been cleared', 'success')
	return show_messages(messages)


#admin function
@app.route('/delete', methods=['POST'])
def delete_message():
	if is_admin():
		uid = request.form['uuid']
		del messages[uid]
		flash(u'Message ' + uid + ' has been deleted', 'success')

		return show_messages(messages)

	return redirect("/")


def is_admin():
	if 'authenticated' not in session.keys():
		session['authenticated'] = False
		return False

	if session['authenticated'] == True:
		return True

	return False


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
