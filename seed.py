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
        "Capital Goods", "Consulting", "Consumer Non-Durables",
        "Consumer Services", "Consumer Staples", "Education",
        "Financials", "Health Care", "Media", "Technology",
        "Basic Industries", "Consumer Discretionary", "Consumer Durables",
        "Energy", "Finance", "Financial", "Information Technology",
        "Miscellaneous", "Public Utilities"
    ]
    for item in industry_list:

        industry = Industry(item)
    
        db.session.add(industry)
        print("industry loading")
    db.session.commit()
    print("industry loading completed")


def load_company():

    with open ("data.csv") as file:
        data = csv.reader(file, delimiter=',')
        next(file) # skip first line

        for row in data:
            company_name, industry_name = row[1], row[2]
            
            if Company.query.filter_by(name=company_name).first() == None:

                if industry_name and industry_name not in ["#N/A", "n/a"]:
                    company = Company(company_name)
                    company.industry = Industry.query.filter_by(name=industry_name).first()
                    db.session.add(company)
                    print("company loading")
        
                else:
                    company = Company(company_name)
                    db.session.add(company)
                    print("company loading")
        
        db.session.commit()
        print("company loading completed")


def load_salary():

    with open ("data.csv") as file:
        data = csv.reader(file, delimiter=',')
        next(file) # skip first line
        
        for row in data:
            company_name, job_title, salary, location, date = row[1], row[6], row[7], row[8], row[11]
            date = datetime.datetime.strptime(date, "%m-%d-%y")
            salary = Salary(date, job_title, int(salary), location)
            salary.company = Company.query.filter_by(name=company_name).first()
            db.session.add(salary)
            print("salary loading")

        db.session.commit()    
        print("salary loading completed")


def load_insterest():
    """load insterst datas and add it to database."""

    trend = TrendReq(hl='en-US', tz=360) # connect to google trends
   
    for company in Company.query.all():
        
        if company.company_id <= 1300:
            continue

        if 1301 <= company.company_id <= 1700:
            kw_list = [] # set keyword
            kw = company.name.lower()
            kw_list.append(kw)

            trend.build_payload(kw_list, timeframe='today 5-y') # build pay load

        # returns historical, indexed data for when the keyword was searched most as shown on Google Trends' Interest Over Time section.
        # return type : pandas dataframe
            trend_df = trend.interest_over_time() 
            trend_df = trend_df.iloc[:,:1] # get rid of isPartial column

            if not trend_df.empty: 
                for row in trend_df.iterrows():
                
                    date, value = row[0], row[1] # date : datetime / interest : pandas series.
                    value = value.to_dict()
                    interest = Interest(date=date, interest=value[kw])
                    interest.company = Company.query.filter_by(name=company.name).first()
                    
                    db.session.add(interest)
                    db.session.commit()
                    print("interest loading")

        else: 
            print("interest loading completed")
            break

        
        print("end of for loops")




if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    #db.create_all()

    # Import different types of data
    #load_industry()
    #load_company()
    #load_salary()
    load_insterest()



