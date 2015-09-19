import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'DQCSUH8E0u'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tmp/hh.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
