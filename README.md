# Groupformer
A tool to make forming groups based on preference more efficient.

1. Install Python 3.8  
1. Install the requirments.txt file:
   - `pip install -r requirments.txt` to install the requirments needed to run our application.
1. To run the tests:
   NOTE for running tests: You need to download the selenium webdriver and put it in your PATH variable.
   
   The requirements.txt reflects the Selenium version used to test the AJAX interaction within groupformer_list, and the form submission interaction within response_screen.
   The WebDriver used for the Selenium test is geckodriver, a Firefox webdriver. 
   Tester must have Firefox installed and install the geckodriver executable ([link](https://github.com/mozilla/geckodriver/releases)) and include its path on the system PATH run out integration tests.

   Run all tests from the project root directory using:
   
   `python manage.py test`

1. After running  you can look at the output in localhost:8000 in your browser by running the following commands 
   - `python manage.py runserver` will run the server on localhost at port 8000
1. Link for project video: https://youtu.be/6ikItt-gD0c
2. Link for live application: https://groupformer.herokuapp.com/
