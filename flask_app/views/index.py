"""
Insta485 index (main) view.
URLs include:
/
"""
import email
import hashlib
import pathlib
import uuid
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
    auth = "None"
    if 'email' in flask.session:
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
    context = {"coaches": coaches, "women": womens_team, "men": mens_team, "auth":auth,}
    return flask.render_template("roster.html",**context)
@flask_app.app.route('/about')
def show_about():
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
    context = {"auth":auth}
    return flask.render_template("about.html",**context)

@flask_app.app.route('/contact')
def show_contact():
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
    context = {"auth":auth}
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
    if len(encrypted_password) == 1:
        flask.session['email'] = username
        return flask.redirect("/")
    cur = connection.execute(
    "SELECT password "
    "FROM wrestlers "
    "WHERE email = ? ",
    (username,)
    )
    encrypted_password = cur.fetchall()
    if len(encrypted_password) == 0:
        return flask.redirect("/log_in")
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
    return flask.send_from_directory(flask_app.app.config['UPLOAD_FOLDER'], url)

@flask_app.app.route('/delete', methods = ['POST'])
def delete():
    email = flask.session["email"]
    name = flask.request.form['username']
    connection = flask_app.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM admins "
        "WHERE fullname = ? ",
        (name,)
    )
    val = cur.fetchall()
    if len(val) > 0:
        val = val[0]
        connection.execute(
            "DELETE FROM admins "
            "WHERE fullname = ? ",
            (name,)
        )
        if val["email"] == email:
            return flask.redirect("/")
        else:
            return flask.redirect("/roster")
    cur = connection.execute(
        "SELECT * "
        "FROM wrestlers "
        "WHERE fullname = ? ",
        (name,)
    )
    val = cur.fetchall()
    if len(val) > 0:
        val = val[0]
        connection.execute(
            "DELETE FROM wrestlers "
            "WHERE fullname = ? ",
            (name,)
        )
        return flask.redirect("/roster")
    return flask.abort(400)


@flask_app.app.route("/add_wrestler")
def add_wrestler():
    context = {}
    return flask.render_template("add_wrestler.html",**context)

@flask_app.app.route("/add_coach")
def add_coach():
    context = {}
    return flask.render_template("add_coach.html",**context)

@flask_app.app.route("/add", methods=['POST'])
def add():
    if flask.request.form['operation'] == "add_wrestler":
        name = flask.request.form['fullname']
        email = flask.request.form['email']
        gender = flask.request.form['gender']
        weight = flask.request.form['weight']
        year = flask.request.form['year']
        password = flask.request.form['password']
        photo = flask.request.files['file']
        photo = save_image(photo)
        password = encrypt_password(password)
        connection = flask_app.model.get_db()
        cur = connection.execute(
            "SELECT * "
            "FROM wrestlers "
            "WHERE fullname = ? ",
            (name,)
        )
        matching = cur.fetchall()
        if len(matching) > 0:
            flask.abort(409)
        cur = connection.execute(
        "INSERT INTO wrestlers"
        "(fullname, pic, weight_class, gender, year, email, password)"
        "VALUES (?,?,?,?,?,?,?)",
        (name, photo, weight, gender, year,email,password,)
        )
        return flask.redirect('/roster')
    if flask.request.form['operation'] == "add_coach":
        name = flask.request.form['fullname']
        email = flask.request.form['email']
        position = flask.request.form['position']
        password = flask.request.form['password']
        photo = flask.request.files['file']
        photo = save_image(photo)
        password = encrypt_password(password)
        connection = flask_app.model.get_db()
        cur = connection.execute(
            "SELECT * "
            "FROM admins "
            "WHERE fullname = ? ",
            (name,)
        )
        matching = cur.fetchall()
        if len(matching) > 0:
            flask.abort(409)
        cur = connection.execute(
        "INSERT INTO admins"
        "(fullname, pic, position, email, password)"
        "VALUES (?,?,?,?,?)",
        (name, photo, position, email, password)
        )
        return flask.redirect('/roster')
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

def save_image(file):
    """Save image to disk."""
    filename = file.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    path = flask_app.app.config["UPLOAD_FOLDER"]/uuid_basename
    file.save(path)
    return uuid_basename

def encrypt_password(password):
    """Encrypt user's password."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string