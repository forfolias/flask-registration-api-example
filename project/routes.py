import re
from flask import json, request
from flask_mail import Mail, Message
from . import app, db


@app.errorhandler(404)
def not_found(error):
    return json.dumps({'status': 'fail', 'message': 'Not found'}), 404


@app.route('/register', methods=["POST"])
def register():
    # check request params
    if "name" not in request.form or "email" not in request.form or not request.form['name'] or not request.form['email']:
        return json.dumps({'status': 'fail', 'message': 'Both name and email are required'}), 422

    # get request params
    name = request.form['name']
    email = request.form['email']

    # email address validation
    if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) == None:
        return json.dumps({'status': 'fail', 'message': 'Invalid email address'}), 422

    # search for existing user
    existing_user = models.User.query.filter_by(email=email).first()
    if existing_user:
        return json.dumps({'status': 'fail', 'message': 'User already registered.'}), 422

    # create User model
    user = models.User(
        name=name,
        email=email
    )

    # store user
    db.session.add(user)
    db.session.commit()

    # send email notification
    mail = Mail(app)
    msg = Message('New registration', sender='registration@project.com',
                  recipients=[app.config['REGISTRATION_MAIL_NOTIFY']])
    msg.body = "A new user registered: " + name + " <" + email + ">"
    try:
        mail.send(msg)
    except Exception as e:
        return json.dumps({'status': 'success', 'message': 'Failed to send email notification'})

    return json.dumps({'status': 'success', 'message': 'User added successfully'})


from . import models
