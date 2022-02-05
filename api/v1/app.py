'''Entry point for the app'''
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST') or '0.0.0.0'
port = getenv('HBNB_API_PORT') or 5000


@app.teardown_appcontext
def teardown_appcontext(self):
    '''This method marked with teardown_appcontext()
    are are called every time the app context tears down.'''
    storage.close()

if __name__ == "__main__":
    app.run(host=host,
            port=port,
            threaded=True)
