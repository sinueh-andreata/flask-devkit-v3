import os
from app import app

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'

    print("running in http://localhost:5555")
    app.run(host='localhost', port=5555, debug=True, use_reloader=True, use_debugger=True)

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'production'
    
    print("running in http://localhost:5777")
    app.run(host='0.0.0.0', port=5777)