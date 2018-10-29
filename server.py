from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import Company, Industry, Interest, Salary, connect_to_db, db
from forms import CompanyForm


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/search')
def select_company():
    """Select Company for search."""

    form = CompanyForm()

    return render_template('company_search_form.html', form=form)

@app.route('/companies')
def companydic():
    """Using for Jquery company name Autocomplete."""

    res = Company.query.all()
    list_companies = [r.as_dict() for r in res]
    return jsonify(list_companies)    


@app.route('/company_view', methods=['POST'])
def salary_view():
    """Create the company's salary table."""
    form = CompanyForm(request.form)
    company_name = form.company.data
    company_name = company_name.upper()
    company = Company.query.filter_by(name=company_name).first()

    if company != None:

        salary_query = company.salaries

        return render_template('form.html', salary_query=salary_query)

    else:

        flash("Please check the company name.")
        return redirect("/form")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    # db.create_all()

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')