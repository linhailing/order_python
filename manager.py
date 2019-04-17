# encoding: utf-8

from application import app, manager
from flask_script import Server
import www


manager.add_command("runserver",Server(host='0.0.0.0', port=8999))

def main():
    manager.run()
    app.DEBUG = True

if __name__ == "__main__":
    try:
        import sys
        sys.exit(main())
    except Exception as e:

        import traceback

        traceback.print_exc()
