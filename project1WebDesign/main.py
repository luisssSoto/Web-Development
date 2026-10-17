from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import os

current_path = os.path.dirname(__file__)
app = Flask(__name__, instance_path=os.path.join(current_path, 'instance'))
SECRET_KEY = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap5(app)
    
@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)