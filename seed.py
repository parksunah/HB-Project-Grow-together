import datetime
from sqlalchemy import func

from model import Company, Industry, Salary, Interest, connect_to_db, db
from server import app


def load_companys():
    """load the data and add it to database."""

    with open ("companylist.txt") as file:

        for row in file:
            row = row.rstrip()
            name, industry = row.split("|")
            name = name.strip()
            industry = industry.strip()

            company = Company(name=name)
            company.industry = db.session.query(Industry).filter_by(name=industry).first()

            db.session.add(company)

    db.session.commit()


def load_salaries():
    """load the salary and add it to database."""

    with open("salarydata.txt") as file:

        for row in file:
            row = row.rstrip()
            date, company_name, job_title, salary, location,  = row.split("|")
            
            # get rid of white space and formating.
            date = date.strip()
            date  = datetime.datetime.strptime(date, "%m/%d/%y")
            company_name = company_name.strip()
            job_title = job_title.strip()
            salary = salary.strip()
            location = location.strip()

            salary = Salary(date, job_title, int(salary), location)
            salary.company = Company.query.filter_by(name=company_name).first()

            db.session.add(salary)

    db.session.commit()


def seed():
    """Set initial fake datas."""
    
    # Industries
    Internet = Industry("Internet")
    Electronics = Industry("Electronics")
    Aerospace_defense = Industry("Aerospace_defense")
    Apparel = Industry("Apparel")
    Automotive = Industry("Automotive")
    Consumer_goods = Industry("Consumer_goods")
    Biotechnology = Industry("Biotechnology")
    Electronics = Industry("Electronics")
    Energy = Industry("Energy")
    Entertainment = Industry("Entertainment")
    Financial = Industry("Financial")

    # Companys
    # Facebook = Company("Facebook")
    # Facebook.industry = Internet
    
    # Google = Company("Google")
    # Google.industry = Internet

    # Fitbit = Company("Fitbit")
    # Fitbit.industry = Electronics

    # Salaries
    # s1 = Salary("2018-10-01", 100000, "San Francisco", "Software engineer")
    # s1.company = Facebook    

    # s2 = Salary("2018-10-02", 95000, "San Jose", "Software engineer")
    # s2.company = Google

    # s3 = Salary("2018-10-03", 90000, "Palo Alto", "Accounting Manager")
    # s3.company = Fitbit

    # # Interests
    # i1 = Interest("2018-10-01", 20)
    # i1.company = Fitbit

    # i2 = Interest("2018-10-02", 30)
    # i2.company = Fitbit
    
    # i3 = Interest("2018-10-03", 40)
    # i3.company = Facebook
    
    # i4 = Interest("2018-10-03", 25)
    # i4.company = Google


    # db.session.add_all([Internet, Electronics, Facebook, Google, Fitbit, s1, s2, s3, i1, i2, i3, i4])
    db.session.add_all([Internet, Electronics, Aerospace_defense, 
                        Apparel, Automotive, Consumer_goods, Biotechnology, 
                        Electronics, Energy, Entertainment, Financial])
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    seed()
    load_companys()
    load_salaries()



