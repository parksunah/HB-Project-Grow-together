from jinja2 import StrictUndefined
import json
from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os
from datetime import datetime, timedelta

from model import Company, Industry, Interest, Salary, connect_to_db, db
from forms import CompanyForm
from job_listings_scraper import get_job_listings


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def select_company():
    """Select Company for search."""

    form = CompanyForm()

    return render_template("home.html", form=form)

@app.route("/companies")
def companydic():
    """Company name search form autocomplete."""

    res = Company.query.all()
    list_companies = [r.as_dict() for r in res]
    return jsonify(list_companies)    


@app.route("/company_view")
def create_main_view():
    """Create the company's salary table."""
 
    try:

        start = datetime.now() # for checking runtime
        form = CompanyForm(request.args)
        company_name = form.company.data
        company_name = company_name.upper()
        company = Company.query.options(
                    db.joinedload("industry")
                    ).filter_by(name=company_name).first()
        print('#' * 20, 'query', datetime.now() - start) # for checking runtime
 
        company_infos = get_company_infos(company_name)
        print('#' * 20, 'infos', datetime.now() - start) # for checking runtime
        
        location=get_maps(company_name)
        print('#' * 20, 'map', datetime.now() - start) # for checking runtime
        print(location)

        job_listings = get_job_listings(company_name)
        print('#' * 20, 'job_listings', datetime.now() - start) # for checking runtime

 
        if company.interest:
            interest_chart=create_interest_chart(company)
            print('#' * 20, 'chart', datetime.now() - start) # for checking runtime
            interest_growth = get_interest_growth(company)
            print('#' * 20, 'interest_growth', datetime.now() - start) # for checking runtime

            if company.ranking:
                ranking = company.ranking
                industry_name = company.industry.name
                industry_num = get_industry_num(industry_name)
                print('#' * 20, 'industry_num & ranking', datetime.now() - start) # for checking runtime

            else:
                industry_name, industry_num, ranking = None, None, None 

        else:
            interest_chart, interest_growth, ranking, industry_name, industry_num = None, None, None, None, None

        return render_template( "main.html",
                                map_key=os.environ['MAP_KEY'],
                                form=form,
                                location=location,
                                salary_query=company.salaries, 
                                company_name=company_name, 
                                job_listings=job_listings,
                                interest_growth=interest_growth,
                                ranking=ranking, 
                                industry_name=industry_name,
                                industry_num=industry_num, 
                                company_infos=company_infos,
                                interest_chart=interest_chart)

    except AttributeError:

        flash("Please check the company name.")
        return redirect("/")

    except TypeError:

        flash("Something else went wrong.")


def get_industry_num(industry_name):
    """Get number of companies which have both a industry and a interest ranking.""" 

    industry = Industry.query.filter_by(name=industry_name).first()
    companies = Company.query.filter(Company.industry_id==industry.industry_id, 
                                                          Company.ranking!=None).order_by(Company.ranking).all()

    return len(companies)


def create_interest_chart(company):
    """Google trends interest chart generator."""
    
    interest = sorted(company.interest, key=lambda x: x.date)
    chart_dic = { 
                  "label1": [ datetime.strftime(obj.date, "%b-%d-%Y") for obj in interest ],
                  "label2": [ obj.interest for obj in interest ]
                }
          
    return chart_dic


def get_interest_growth(company):
    """Get the interest ranking in the same industy companies."""

    interest = sorted(company.interest, key=lambda x: x.date)

    interest_start = interest[0]
    interest_end = interest[-1]

    # preventing for division by zero error.
    if interest_start.interest == 0:
        interest_growth = (interest_end.interest - 1) / 1 * 100
        
    else:
        interest_growth = (interest_end.interest - interest_start.interest) / interest_start.interest * 100

    return interest_growth


def get_company_infos(company_name):
    """Get Company's desc and logo img with Bing API."""

    import pprint 

    subscription_key = os.environ['BING_KEY'] 
    assert subscription_key

    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    search_term = company_name.lower()+" company profile"

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key, "Content-Type": "application/json; charset=utf-8"}
    params  = {"q": search_term, "textDecorations":True}
    response = requests.get(search_url, headers=headers, params=params)
    search_results = response.json()
    pprint.pprint(search_results)

    try:
        company_desc = search_results['entities']['value'][0]['description']
        try:
            company_img = search_results['entities']['value'][0]['image']['thumbnailUrl']

        except KeyError:
            # If API have a 'entities' field, but doesn't have a 'image' field.
            company_img = None

        #print(company_img)
        #print(company_desc)

        return (company_desc, company_img)

    except KeyError:
        # If API doesn't have a 'entities' field.
        try:
            company_desc = search_results['webPages']['value'][1]['snippet']
            company_desc = company_desc.replace("\ue000", "") # delete special characters.
            company_desc = company_desc.replace("\ue001", "") # delete special characters.

            return (company_desc, None)

        except: 
            # If API can't find any information.
            return (None, None)


@app.route("/news.json")
def get_news():
    """Get the news for specific date, 
    when user click the interest chart's specific point."""
    
    news_key = os.environ['NEWS_KEY']

    cap_company_name = request.args.get("company_name")
    company_name = cap_company_name.lower()

    news_date = request.args.get("from")
    from_date = datetime.strptime(news_date, "%b-%d-%Y")
    to_date = from_date + timedelta(6)

    url = "https://newsapi.org/v2/everything"
    
    headers = {"Content-Type": "application/json; charset=utf-8"}

    params  = { 
            "q": company_name, 
            "from": from_date,    
            "to": to_date,
            "sortBy" : "relevancy",
            "apiKey" : news_key,
            "language":"en"
            }

    try:
        response = requests.get(url, headers=headers, params=params)
        print(response.url)

        return jsonify(response.json()['articles'])

    except KeyError:
        return None


def get_maps(company_name):
    """Create company's HQ location using google map."""

    map_key = os.environ['MAP_KEY']

    company = Company.query.options(
                db.joinedload("salaries")
                ).filter_by(name=company_name).first()

    postal_code = company.salaries[0].work_site_postal_code

    # Use work site postal code in db.
    url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json")
    params = { "input" : company_name +", "+ postal_code,
               "inputtype" : "textquery",
               "fields":"photos,formatted_address,name,rating,opening_hours,geometry",
               "key": map_key } 

    headers = {'Content-Type': 'application/json; charset=utf-8'}

    response = requests.get(url, headers=headers, params=params)
    
    r = response.json()
    
    if r['status'] == 'ZERO_RESULTS':
        # Just use hq_address in db.
        hq_address = company.hq_address
        params = { "input" : hq_address,
                    "inputtype" : "textquery",
                    "fields":"photos,formatted_address,name,rating,opening_hours,geometry",
                    "key":map_key} 
        response = requests.get(url, headers=headers, params=params)

        r = response.json()

    location = {"name" : r['candidates'][0]['name'], 
                "address": r['candidates'][0]['formatted_address'],
                "lat" : r['candidates'][0]['geometry']['location']['lat'],
                "lng" : r['candidates'][0]['geometry']['location']['lng']}
    print(location)

    return location


@app.route("/interest_ranking")
def create_interest_ranking_page():
    """Create google interest ranking page in each industry sector."""

    industry_name = request.args.get("industry_name")

    company = Company.query.options(
                    db.joinedload("industry")
                      ).filter_by(industry_name=industry_name).order_by(Company.desc).all()

    return render_template("interest_ranking.html", industry=industry)


@app.route("/interest_view/<industry_name>")
def create_interest_ranking_view(industry_name):
    """Interest growth ranking page in each industry sector."""

    industry = Industry.query.filter_by(name=industry_name).first()
    industries = Industry.query.all()   
    companies = Company.query.filter(Company.industry_id==industry.industry_id, Company.ranking!=None).order_by(Company.ranking).all()

    return render_template("interest_ranking.html", companies=companies, industries=industries)


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