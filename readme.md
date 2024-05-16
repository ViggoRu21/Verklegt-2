# Job hunters
*Salary Sleuth* is our website for the course T-220-VLN2.

In it we completed all the core requirements given in the assignment description.
As well as these extra requirements:
- TODO


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
