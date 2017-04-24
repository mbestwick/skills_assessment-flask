from flask import Flask, request, render_template, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/")
def index():
    """ Homepage. """

    return render_template("index.html")


@app.route("/application-form")
def fill_out_application():
    """ Returns page with job application form. """

    available_jobs = [
        "Software Engineer",
        "QA Engineer",
        "Product Manager"
        ]

    return render_template("application-form.html", jobs=available_jobs)


@app.route("/application-success", methods=["POST"])
def completed_application():
    """ Returns response page with acknowledgement of application. """

    session['first_name'] = request.form.get("firstname")
    session['last_name'] = request.form.get("lastname")
    session['job'] = request.form.get("job")

    try:
        session['salary'] = int(request.form.get("salary"))
    except:
        flash("Please enter a number for salary, no commas")
        return redirect("/application-form")

    if not session['job']:
        flash("Please choose a job!")
        return redirect("/application-form")

    return render_template(
        "application-response.html",
        first_name=session['first_name'],
        last_name=session['last_name'],
        job=session['job'],
        salary=session['salary'])


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host="0.0.0.0")
