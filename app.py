from flask import *
from forms import RegistrationForm, LoginForm
import logging

logging.basicConfig(level="DEBUG")

app = Flask(__name__)
app.config['SECRET_KEY'] = '79d0f69fc13be5944aab2a4e096f501c4a70a426f15c661f0467d276c255d3ff'

postz = [
    {
        'author': 'corey qedcsx',
        'title': 'blog post 1',
        'content': 'First post',
        'date_posted': 'april 13,1222'
    },
    {
        'author': 'corey qedcsx 2',
        'title': 'blog post 2',
        'content': 'Second post',
        'date_posted': 'april 16,1222'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", postz=postz, title="ebvhls")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        logging.debug("form validated")
        # success - is bootstrap part
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    logging.debug("form not validated")
    return render_template('register.html', title="Login", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)



if __name__ == "__main__":
    app.run(debug=True)


