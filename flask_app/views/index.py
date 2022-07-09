"""
Insta485 index (main) view.
URLs include:
/
"""
import email
import hashlib
import flask
import flask_app
@flask_app.app.route('/')
def show_index():
    """Display / route."""
    auth = "None"
    if 'email' in flask.session:
        connection = flask_app.model.get_db()
        email = flask.session['email']
        cur = connection.execute(
            "SELECT * "
            "FROM admins "
            "WHERE email = ?",
            (email,)
        )
        info = cur.fetchall()
        if len(info) > 0:
            auth = "Admin"
        cur = connection.execute(
            "SELECT * "
            "FROM wrestlers "
            "WHERE email = ?",
            (email,)
        )
        info = cur.fetchall()
        if len(info) > 0:
            auth = "Wrestler"
    context = {'auth': auth}
    return flask.render_template("index.html", **context)

@flask_app.app.route('/roster')
def show_roster():
    connection = flask_app.model.get_db()
    cur = connection.execute(
            "SELECT * "
            "FROM admins "
        )
    coaches = cur.fetchall()
    cur = connection.execute(
            "SELECT * "
            "FROM wrestlers "
            "WHERE gender = 'F'"
        )
    womens_team = cur.fetchall()
    womens_team = sorted(womens_team, key=lambda k: k['weight_class'], reverse=False)
    cur = connection.execute(
            "SELECT * "
            "FROM wrestlers "
            "WHERE gender = 'M'"
        )
    mens_team = cur.fetchall()
    mens_team = sorted(mens_team, key=lambda k: k['weight_class'], reverse=False)
    context = {"coaches": coaches, "women": womens_team, "men": mens_team}
    return flask.render_template("roster.html",**context)
@flask_app.app.route('/about')
def show_about():
    context = {}
    return flask.render_template("about.html",**context)

@flask_app.app.route('/contact')
def show_contact():
    context = {}
    return flask.render_template("contact.html",**context)

@flask_app.app.route('/log_in')
def show_login():
    context={}
    return flask.render_template("login.html",**context)

@flask_app.app.route('/login', methods=['POST'])
def login():
    username = flask.request.form['email']
    if username is None:
        flask.abort(400)
    password = flask.request.form['password']
    if password is None:
        flask.abort(400)
    connection = flask_app.model.get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM admins "
        "WHERE email = ? ",
        (username,)
    )
    encrypted_password = cur.fetchall()
    if len(encrypted_password) == 0:
        cur = connection.execute(
        "SELECT password "
        "FROM wrestlers "
        "WHERE email = ? ",
        (username,)
    )
    encrypted_password = cur.fetchall()
    encrypted_password = encrypted_password[0]['password']
    lst = encrypted_password.split('$')
    salt = lst[1]
    if check_password(password, salt, encrypted_password):
        flask.session['email'] = username
        return flask.redirect("/")
    else:
        return flask.redirect("/log_in")
@flask_app.app.route('/uploads/<url>')
def get_image(url):
    """Get image for page."""
    print("TESTING :)")
    print(url)
    return flask.send_from_directory(flask_app.app.config['UPLOAD_FOLDER'], url)


def check_password(password, salt, real):
    """Check password."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    if password_db_string == real:
        return True
    return False