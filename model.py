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

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hq_address = db.Column(db.String, nullable=False)
    interest_growth = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    industry_id = db.Column(db.Integer, db.ForeignKey("industries.industry_id"), nullable=True)

    industry = db.relationship("Industry", backref=db.backref("companies"))

    def __init__(self, name, hq_address):
        self.name = name
        self.hq_address = hq_address
        

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Company company_id={self.company_id}, industry_id={self.industry_id}, name={self.name}, interest_growth={self.interest_growth}, ranking={self.ranking}, hq_address={self.hq_address}>"

    def as_dict(self):

        return {"name": self.name}


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

    def as_dict(self):

        return {"name": self.name}



class Interest(db.Model):
    """Interest from google trends."""

    __tablename__ = "interest"

    interest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    interest = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"), nullable=False)

    company = db.relationship("Company", backref=db.backref("interest"))

    def __init__(self, date, interest):
        self.date = date
        self.interest = interest

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Interest interest_id={self.interest_id}, company_id={self.company_id}, date={self.date}, interest={self.interest}>"


class Salary(db.Model):
    """Salary data from labor department."""

    __tablename__ = "salaries"

    salary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, unique=False)
    job_title = db.Column(db.String, nullable=False, unique=False)
    salary = db.Column(db.Integer, nullable=False, unique=False)
    work_site_city = db.Column(db.String, nullable=False, unique=False)
    work_site_postal_code = db.Column(db.String, nullable=False, unique=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"), nullable=False)

    company = db.relationship("Company", backref=db.backref("salaries"))

    def __init__(self, date, job_title, salary, work_site_city, work_site_postal_code):
        self.date = date
        self.job_title = job_title
        self.salary = salary
        self.work_site_city = work_site_city
        self.work_site_postal_code = work_site_postal_code
        

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Salary salary_id={self.salary_id}, company_id={self.company_id}, date={self.date}, job_title={self.job_title}, salary={self.salary}, work_site_city={self.work_site_city}, work_site_postal_code={self.work_site_postal_code}>"



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///insideout"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")   

    




