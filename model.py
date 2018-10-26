"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy



# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Company(db.Model):
    """Company searching for."""

    __tablename__ = "companys"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey("industries.industry_id"), nullable=False)
    desc = db.Column(db.String, nullable=True)

    industry = db.relationship("Industry", backref=db.backref("companys"))

    def __init__(self, name):
        self.name = name
        

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Company company_id={self.company_id} name={self.name}>"



class Industry(db.Model):
    """Industry sector that company belongs to."""

    __tablename__ = "industries"

    industry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Industry industry_id={self.industry_id} name={self.name}>"



class Interest(db.Model):
    """Interest from google trends."""

    __tablename__ = "interests"

    interest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    interest = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companys.company_id"), nullable=False)

    company = db.relationship("Company", backref=db.backref("interests"))

    def __init__(self, date, interest):
        self.date = date
        self.interest = interest

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Interest interest_id={self.interest_id}, date={self.date}, interest={self.interest}, company_id={self.company_id}>"


class Salary(db.Model):
    """Salary data from labor department."""

    __tablename__ = "salaries"

    salary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companys.company_id"), nullable=False)

    company = db.relationship("Company", backref=db.backref("salaries"))

    def __init__(self, date, salary, location, job_title):
        self.date = date
        self.salary = salary
        self.location = location
        self.job_title = job_title

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Salary salary_id={self.salary_id}, date={self.date}, salary={self.salary}, location={self.location}, job_title={self.job_title}, company_id={self.company_id}>"



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///grow"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")   




