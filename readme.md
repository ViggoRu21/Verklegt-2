# Job hunters
*Salary Sleuth* is our website for the course T-220-VLN2.

In it we completed all the core requirements given in the assignment description.
As well as these extra requirements:
- We have a company side og the website
  - Where they can log in
  - View their listings
- When a company account tries to log in as an applicant the site redirects
- We have a site listing all companies
- Edit profile (more then required)
- Order by salary high to low and low to high
- 


## Usage
### To run the website you must

Set up a virtual environment:

`python -m venv env`

`source env/bin/activate `

Install the necessary dependencies:

`pip install -r requirements.txt`

Start the server:

`python manage.py runserver`

Then the website should be running on http://localhost:8000/

## The data
In this assignment we utilized a way to generate fake data as you can see in our *scripts* folder.

Note: The database is already loaded with this data. Running the data generation script again is not necessary but can be done if desired:

`python scripts/create_fake_data.py`

This data is fully randomly generated and is not supposed to be fully accurate and correct. It is intended to show the functionality of the website.
We generated all data, including resumes, company logos and applicant images randomly.

## Simplify your overview
You can always register an account and go through each step yourself 
but you can also log into any recruiter/applicant in currently in the database with the password "pw".

### Our applicants
- hdeleon
- helen
- lisa86
- lwatkins
- rogerslaura
- angelamorris
- wilcoxalexis
- hansenemily
- carolkaiser
- brian96

### Our Recruiters 
- brian96
- matthew93
- ian70
- amywilliams
- fjohnson

#### Company ssn's
Here are company ssn's which can be used to create new recruiter accounts.
- 197244-3111
- 537377-1719
- 867965-0085
- 574731-8333
- 466706-6803


