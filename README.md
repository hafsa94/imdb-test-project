# imdb-test-project

Requirements:
----------------------------------------------------------------------------------------------

As a user I want to fetch name, ratings and movie release year of top 250 movies from IMDB website and store the result in SQLite database
As a user I want to Print database results

Write desired test cases for above requirements and design and implement a test automation for executing the same.

1) Use Page Object Modelling.
2) Use any language (Java/Ruby/Python etc) supported by Selenium WebDriver.
3) Integrate with any build/project automation tool like gradle,bundler,maven etc.

Solution:
----------------------------------------------------------------------------------------------

For successfully running the Automated Test Cases, install all the dependency as follow:

1. Go to ~/imdb-test-project/upgrad_testing/test_requirements 
2. Run command --->  pip install -r testing_requirements.txt

After installing the dependencies, to run the test case follow below step:

1. Go to ~/imdb-test-project/upgrad_testing/test_class 
2. Run command  --->  nosetests --verbosity=3 --nologcapture --nocapture

For more nose plugins refer http://nose.readthedocs.io/en/latest/usage.html

NOTE: Please perform all the commands in an virtual environment
