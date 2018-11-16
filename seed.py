import datetime
from sqlalchemy import func
from pytrends.request import TrendReq
import pandas as pd
import csv

from model import Company, Industry, Salary, Interest, connect_to_db, db
from server import app


def load_industry():
    """Set industry datas."""
    
    industry_list = [
        "Advertising & Marketing", "Aerospace & Defense", "Basic Industries",
        "Business Products & Services", "Chemicals", "Computer Hardware", 
        "Consumer Products & Services", "Education", "Energy", "Engineering", 
        "Environment & Weather", "Finance", "Food & Beverage", "Governance", 
        "Health Care", "Human Resources", "Industrials", "Insurance", "Media", 
        "Miscellaneous", "Motor Vehicles & Parts", "Real Estate", "Retail", 
        "Scientific Research", "Security", "Technology", "Telecommunications", 
        "Transportation", "Travel & Hospitality", "Utilities"
    ]
    for item in industry_list:

        industry = Industry(item)
    
        db.session.add(industry)
        print("industry loading")
    db.session.commit()
    print("industry loading completed")


def load_company():

    with open ("data.csv") as file:
        data = csv.reader(file, delimiter=",")
        next(file) # skip first line

        for row in data:
            company_name, industry_name, hq_address = row[2].strip(), row[8].strip(), row[3].strip()+", "+ row[4].strip() +", "+ row[5].strip()
            
            if Company.query.filter_by(name=company_name).first() == None:

                if industry_name:
                    company = Company(company_name, hq_address)
                    company.industry = Industry.query.filter_by(name=industry_name).first()
                    db.session.add(company)
                    print("company loading")
        
                else:
                    company = Company(company_name, hq_address)
                    db.session.add(company)
                    print("company loading")
        
        db.session.commit()
        print("company loading completed")


def load_salary():

    with open ("data.csv") as file:
        data = csv.reader(file, delimiter=",")
        next(file) # skip first line
        
        for row in data:
            company_name, job_title, salary, date, work_site_city, postal_code = row[2].strip(), row[6].strip(), row[7].strip(), row[1].strip(), row[9].strip(), row[12].strip()
            date = datetime.datetime.strptime(date, "%m-%d-%y")
            salary = Salary(date, job_title, int(salary), work_site_city, postal_code)
            salary.company = Company.query.filter_by(name=company_name).first()
            db.session.add(salary)
            print("salary loading")

        db.session.commit()    
        print("salary loading completed")


def load_interest():
    """load insterst datas and add it to database."""

    trend = TrendReq(hl="en-US", tz=360) # connect to google trends
   
    i = 3151
    while i <= 3300:

        company = Company.query.get(i)
        kw_list = [] # set keyword
        kw = company.name.lower()
        print(kw)
        kw_list.append(kw)
        trend.build_payload(kw_list, timeframe="2015-11-10 2018-11-11")
        trend_df = trend.interest_over_time()
        print(trend_df)
        trend_df = trend_df.iloc[:,:1]

        if not trend_df.empty:
            for row in trend_df.iterrows():
                date, value = row[0], row[1] # date : datetime / interest : pandas series.
                value = value.to_dict()
                interest = Interest(date=date, interest=value[kw])
                interest.company = Company.query.filter_by(name=company.name).first()
                db.session.add(interest)
                db.session.commit()
            print(f"{company.company_id} saved.")
        else:
            print(f"{company.company_id} not found.")
        i += 1

    print("interest loading completed")


def get_interest_growth(company):
    """Get the interest ranking in the same industy companies."""

    interest = sorted(company.interest, key=lambda x: x.date)
    interest_start = interest[0]
    interest_end = interest[-1]

    # preventing for division by zero error.
    if interest_start.interest == 0:
        if interest_end.interest != 0:
            interest_growth = (interest_end.interest - 1) / 1 * 100
        else:
            interest_growth = 0        
    else:
        interest_growth = (interest_end.interest - interest_start.interest) / interest_start.interest * 100

    return interest_growth


def _save_interest_growth_ranking_to_db(industry_id):
    """Get the interest movement ranking in the same industry and store it to db."""

    growth_list = []
    company_list = []

    industry = Industry.query.options(
        db.joinedload("companies")
    ).filter_by(industry_id=industry_id).first()

    for company in industry.companies:

        if company.interest:
            company_interest_growth = get_interest_growth(company)
            growth_list.append(company_interest_growth)
            company_list.append(company)
        else:
            print(f"{company.company_id} has no interest.")
        
    sorted_growth_list = sorted(growth_list, reverse=True)
    print(sorted_growth_list)

    for company in company_list:
        ranking = sorted_growth_list.index(get_interest_growth(company))
        print((ranking+1), company.name, company.company_id, get_interest_growth(company))
        company.ranking = ranking+1
        #print(company.ranking)
        db.session.commit()


def _save_sorted_interest_growth_ranking_to_db(industry_id):
    """If company has 0 interest during first 10 weeks and last 10 weeks, exclude it from ranking."""

    growth_list = []
    company_list = []

    industry = Industry.query.options(
                 db.joinedload("companies")
               ).filter_by(industry_id=industry_id).first()

    for company in industry.companies:

        if company.interest:
            interest_list = [ i.interest for i in sorted(company.interest, key=lambda x: x.date) ]
            
            if (0 in interest_list[:20]) and (0 in interest_list[136:]):
                print(f"{company.company_id} has 0 interest during first 10 weeks and last 10 weeks.")
                
            else:
                company_interest_growth = get_interest_growth(company)
                growth_list.append(company_interest_growth)
                company_list.append(company)
        else:
            print(f"{company.company_id} has no interest.")
        
    sorted_growth_list = sorted(growth_list, reverse=True)
    print(sorted_growth_list)

    for company in company_list:
        ranking = sorted_growth_list.index(get_interest_growth(company))
        print((ranking+1), company.name, company.company_id, get_interest_growth(company))
        company.ranking = ranking+1
        #print(company.ranking)
        db.session.commit()

def _ranking_cleaner(industry_id):

    industry = Industry.query.options(
                  db.joinedload("companies")
               ).filter_by(industry_id=industry_id).first()

    for company in industry.companies:  

        if company.ranking:
            company.ranking = None
            db.session.commit()



def _save_interest_growth_to_db(industry_id):
    """Get the interest ranking in the same industy companies."""

    all_company = Company.query.filter_by(industry_id=industry_id).all()

    for company in all_company:

        if company.interest:

            interest = sorted(company.interest, key=lambda x: x.date)
            interest_start = interest[0]
            interest_end = interest[-1]

            # preventing for division by zero error.
            if interest_start.interest == 0:
                if  interest_end.interest != 0:
                    interest_growth = (interest_end.interest - 1) / 1 * 100
                else:
                    interest_growth = 0
            else:
                interest_growth = (interest_end.interest - interest_start.interest) / interest_start.interest * 100

            company.interest_growth = float(interest_growth)
            db.session.commit()
            print(f"{company.company_id} saved.")

        else:
            print(f"{company.company_id} has no interest data.")


    print("Interest growth saved completely.") 


def _save_interest_growth_to_db_by_company_id(company_id):
    """Get the interest ranking in the same industy companies."""

    all_company = Company.query.filter_by(company_id=company_id).all()

    for company in all_company:

        if company.interest:

            interest = sorted(company.interest, key=lambda x: x.date)
            interest_start = interest[0]
            interest_end = interest[-1]

            # preventing for division by zero error.
            if interest_start.interest == 0:
                if  interest_end.interest != 0:
                    interest_growth = (interest_end.interest - 1) / 1 * 100
                else:
                    interest_growth = 0
            else:
                interest_growth = (interest_end.interest - interest_start.interest) / interest_start.interest * 100

            company.interest_growth = float(interest_growth)
            db.session.commit()
            print(f"{company.company_id} saved.")

        else:
            print(f"{company.company_id} has no interest data.")


    print("Interest growth saved completely.")      



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    #load_industry()
    #load_company()
    #load_salary()
    #load_interest()



