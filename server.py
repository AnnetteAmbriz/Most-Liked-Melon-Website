from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from melons import MOST_LOVED_MELONS


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRETKEY"


@app.route("/")
def index():
    """Return homepage."""
    if 'username' in session:
        return redirect("/top-melons")
    return render_template("homepage.html")

@app.route("/get-name")
def get_person_name():
    """Get name from form on homepage"""
    username = request.args.get("name")
    session['username'] = username
    return redirect("/top-melons")


@app.route("/top-melons")
def display_top_melons():
    """
    Check if name in session if so, display top melons if not
    redirect to "/"
    """
    if 'username' in session:
        return render_template("top-melons.html", melon_dic=MOST_LOVED_MELONS)
    return redirect("/")

@app.route("/love-melon")
def increase_loved_melon():
    if request.method == 'POST':
        users_most_loved_melon = request.form

        MOST_LOVED_MELONS[users_most_loved_melon]['num_loves'] += 1

        return render_template("thank-you.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(host="0.0.0.0")