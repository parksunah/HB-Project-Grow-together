import datetime
from sqlalchemy import func

from model import Company, Industry, Salary, Interest, connect_to_db, db
from flask import Flask
from server import app


def seed():
    """Set initial fake datas."""
    
    # Industries
    Internet = Industry("Internet")
    Electronics = Industry("Electronics")

    # Companys
    Facebook = Company("Facebook")
    Facebook.industry = Internet
    
    Google = Company("Google")
    Google.industry = Internet

    Fitbit = Company("Fitbit")
    Fitbit.industry = Electronics

    # Salaries
    s1 = Salary("2018-10-01", 100000, "San Francisco", "Software engineer")
    s1.company = Facebook    

    s2 = Salary("2018-10-02", 95000, "San Jose", "Software engineer")
    s2.company = Google

    s3 = Salary("2018-10-03", 90000, "Palo Alto", "Accounting Manager")
    s3.company = Fitbit

    # Interests
    i1 = Interest("2018-10-01", 20)
    i1.company = Fitbit

    i2 = Interest("2018-10-02", 30)
    i2.company = Fitbit
    
    i3 = Interest("2018-10-03", 40)
    i3.company = Facebook
    
    i4 = Interest("2018-10-03", 25)
    i4.company = Google


    db.session.add_all([Internet, Electronics, Facebook, Google, Fitbit, s1, s2, s3, i1, i2, i3, i4])
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Initiate instances.
    seed()
