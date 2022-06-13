import os
from app import create_app
from app.databases.deploy_db import deploy_db

app = create_app(os.getenv('FLASK_CONFIG') or 'default') # создание приложения
if __name__ == "__main__":
    deploy_db()
    app.run(debug=True)