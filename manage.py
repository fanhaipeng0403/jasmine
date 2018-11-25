from jasmine_app import create_app
import os

app = create_app(config_name=os.environ.get('ENV', 'default'))

if __name__ == '__main__':
    app.run()
