from app import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=81, threaded=True)



