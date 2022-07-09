"""
Insta485 index (main) view.
URLs include:
/
"""
import flask
import flask_app
@flask_app.app.route('/')
def show_index():
    """Display / route."""
    context = {}
    return flask.render_template("index.html", **context)


@flask_app.app.route('/about')
def show_about():
    context = {}
    return flask.render_template("about.html",**context)

@flask_app.app.route('/contact')
def show_contact():
    context = {}
    return flask.render_template("contact.html",**context)
@flask_app.app.route('/uploads/<url>')
def get_image(url):
    """Get image for page."""
    print("TESTING :)")
    print(url)
    return flask.send_from_directory(flask_app.app.config['UPLOAD_FOLDER'], url)