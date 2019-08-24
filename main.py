from app import app #, db
import view
#from flask import Flask
#from posts.blueprint import posts

#app.register_blueprint(posts, url_prefix='/blog')
#app = Flask(__name__)
#@app.route('/')
#def index():
 #   return 'fd'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int("8080"))
