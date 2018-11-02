from jinja2 import StrictUndefined
import json
from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import Company, Industry, Interest, Salary, connect_to_db, db
from forms import CompanyForm
from lxml import html, etree
import requests
import re
import argparse
import os


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route("/search")
def select_company():
    """Select Company for search."""

    form = CompanyForm()

    return render_template("company_search_form.html", form=form)

@app.route("/companies")
def companydic():
    """Using for Jquery company name Autocomplete."""

    res = Company.query.all()
    list_companies = [r.as_dict() for r in res]
    return jsonify(list_companies)    


@app.route("/company_view")
def create_result_view():
    """Create the company's salary table."""
  
    form = CompanyForm(request.args)
    company_name = form.company.data
    company_name = company_name.upper()
    company = Company.query.options(
        db.joinedload("industry")
          .joinedload("companies")
          .joinedload("interest")
    ).filter_by(name=company_name).first()

    
    job_listings = get_job_listings(company_name)
    company_infos = get_company_infos(company_name)

    if company.industry:
        ranking = get_interest_growth_ranking(company)
        industry_name = company.industry.name
    
    else:
        ranking = None
        industry_name = None

    if company != None:

        salary_query = company.salaries

        return render_template("form.html", salary_query=salary_query, 
                                company_name=company_name, job_listings=job_listings,
                                ranking =ranking, industry_name=industry_name, 
                                company_infos=company_infos)

    else:

        flash("Please check the company name.")
        return redirect("/search")


def get_job_listings(company_name):
    """Glassdoor job postings scraper. source : scrapehero."""
 
    keyword = company_name
    place =  "San Francisco Bay area"

    headers = { 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                'referer': 'https://www.glassdoor.com/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
    }

    location_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'referer': 'https://www.glassdoor.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    data = {"term": place,
            "maxLocationsToReturn": 10}

    location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
    try:
        # Getting location id for search location
        print("Fetching location details")
        location_response = requests.post(location_url, headers=location_headers, data=data).json()
        place_id = location_response[0]['locationId']
        job_litsting_url = 'https://www.glassdoor.com/Job/jobs.htm'
        # Form data to get job results
        data = {
            'clickSource': 'searchBtn',
            'sc.keyword': keyword,
            'locT': 'C',
            'locId': place_id,
            'jobType': ''
        }

        job_listings = []
        if place_id:
            response = requests.post(job_litsting_url, headers=headers, data=data)
            parser = html.fromstring(response.text)
            # Making absolute url 
            base_url = "https://www.glassdoor.com"
            parser.make_links_absolute(base_url)

            XPATH_ALL_JOB = '//li[@class="jl"]'
            XPATH_NAME = './/a/text()'
            XPATH_JOB_URL = './/a/@href'
            XPATH_LOC = './/span[@class="subtle loc"]/text()'
            XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
            XPATH_SALARY = './/span[@class="green small"]/text()'
            XPATH_RATING = './/span[@class="compactStars "]/text()'


            listings = parser.xpath(XPATH_ALL_JOB)
            for job in listings:
                raw_job_name = job.xpath(XPATH_NAME)
                raw_job_url = job.xpath(XPATH_JOB_URL)
                raw_lob_loc = job.xpath(XPATH_LOC)
                raw_company = job.xpath(XPATH_COMPANY)
                raw_salary = job.xpath(XPATH_SALARY)
                raw_rating = job.xpath(XPATH_RATING)

                # Cleaning data
                job_name = ''.join(raw_job_name).strip('–') if raw_job_name else None
                job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
                raw_state = re.findall(",\s?(.*)\s?", job_location)
                state = ''.join(raw_state).strip()
                raw_city = job_location.replace(state, '')
                city = raw_city.replace(',', '').strip()
                company = ''.join(raw_company).replace('–','')
                salary = ''.join(raw_salary).strip()
                rating = ''.join(raw_rating).strip()
                job_url = raw_job_url[0] if raw_job_url else None

                jobs = {
                    "Name": job_name,
                    "Company": company,
                    "State": state,
                    "City": city,
                    "Salary": salary,
                    "Location": job_location,
                    "Url": job_url,
                    "Rating" : rating
                }
                job_listings.append(jobs)

            return job_listings
        else:
            print("location id not available")

    except:
        print("Failed to load locations")


# @app.route("/job_listings.json")
# def _job_listings_convert_to_json():
#     """Convert a list to JSON."""

#     company_name = request.args.get("company_name")

#     return jsonify(get_job_listings(company_name))


@app.route("/interest.json") 
def get_interest():
    """Create interest list using sqlalchemy for chart."""

    company_name = request.args.get("company_name")

    company = Company.query.filter_by(name=company_name).first()
    company_id = company.company_id

    if not company.interest:
        return None

    else:

        data_dict = {
        "labels": [ obj.date.isoformat() for obj in Interest.query.filter_by(company_id=company_id).all()],
        "datasets": [
            {
                "label": company_name,
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(151,187,205,0.2)",
                "borderColor": "rgba(151,187,205,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(151,187,205,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(151,187,205,1)",
                "pointHoverBorderWidth": 2,
                "pointHitRadius": 10,
                "data": [ obj.interest for obj in Interest.query.filter_by(company_id=company_id).all() ],
                "spanGaps": False},
                ]
            }   

        return jsonify(data_dict)


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


def get_interest_growth_ranking(target_company):

    larger = []
    target_interest_growth = get_interest_growth(target_company)

    for company in target_company.industry.companies:

        if company.interest:
            company_interest_growth = get_interest_growth(company)
            if company_interest_growth > target_interest_growth:
                larger.append(company_interest_growth)
            else:
                continue
        else:
            continue


    ranking = len(larger) + 1
    total = len(target_company.industry.companies)

    return ranking, total



def get_company_infos(company_name):
    """Get Company's desc and logo img using Bing API."""

    subscription_key = os.environ['BING_KEY'] # error occurs
    assert subscription_key

    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    search_term = company_name.lower()+" company profile"

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    print(search_results)

    company_desc = search_results['entities']['value'][0]['description']
    company_img = search_results['entities']['value'][0]['image']['thumbnailUrl']

    return (company_desc, company_img)




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