"""Insta485 development configuration."""
import pathlib
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# Secret key for encrypting cookies
SECRET_KEY = b'\x96\xb3\xc0$\x83^\x18E\x07,zn\xa0\xe7Y\x9b\xbbU%&\x82\xc8\x10\xa2'
SESSION_COOKIE_NAME = 'login'
# File Upload to var/uploads/
FLASK_APP_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = FLASK_APP_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
# Database file is var/insta485.sqlite3
DATABASE_FILENAME = FLASK_APP_ROOT/'var'/'insta485.sqlite3'
