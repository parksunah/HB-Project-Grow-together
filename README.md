# Inside Out; Job Seeker’s Best Friend
Inside Out is an web app that provides to job seekers essential company data that are not easily found elsewhere. It uses key APIs including Google Maps API, Bing Web Search API, and News API. It also uses real salary data from U.S Labor Department as well as real time job listings scraped from Glassdoor. By simply typing in a company name, users can get the company overview, employee rating, location, and latest Google search trends visualized through Chart.js. Clicking on specific dates on the trend chart retrieves relevant news. Users can even check and compare company ranking within each industry based on search volume growth.

# Tech Stack
- Python, JavaScript (AJAX, JSON), HTML, CSS, SQL, Flask, jQuery, Bootstrap, Jinja, Chart JS, PostgreSQL, SQLAlchemy, Flask-WTF

# APIs Used
- Google Maps API(Geocode, Maps), Bing Web Search API, News API

# Features
## Homepage
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/1.png?raw=true)

## Main page

### Company Overview
- In this section, company overview including the logo & description is provided through Bing Web Search API. Company's location is also diplayed through Google Maps API. Latest employee rating, scraped real-time from Glassdoor, as well as Google search volume growth ranking within industries are shown here so that users can get a better sense of the company's work environment and overall business health.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/2.png?raw=true)

### Search Volume Trend from Google Trends
- Here, the company's search volume data from Google Trends is visualized through Chart JS. It shows the search trend on Google for the past 3 years. 
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/3.png?raw=true)

### Related News
- This news card generator responds to user's click. When user clicks a point on the chart, Chart JS method is called, and captures date.  Then a request to News API is triggered to loop over JSON results, and generates news card from the specific week.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/4.png?raw=true)

### Real Salary Data from U.S Labor Department
- In this section, users can check out real salary data from U.S Labor Department. This is based on H1B foreign worker filings in 2018. Postgre and SQLAlchemy are used here.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/5.png?raw=true)

### Job Listing from Glassdoor
- This is where jobs posted online are displayed based on real time data from Glassdoor. Because Glassdoor doesn't have a public API anymore, these jobs are fetched through a custom scraper with the Python request and lxml modules to scrape the company's rating and job listings.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/6.png?raw=true)

## Ranking Page
- Search volume growth ranking within same industries is shown here. Eager join (on a db relationship between db tables) and table index (to avoid a full table scan) are used to improve loading time.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/7.png?raw=true)

