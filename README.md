# Groupformer
A tool to make forming groups based on preference more efficient.

1.  Install Python 3.8  
2.  Install the requirments.txt file:
   - `pip install -r requirments.txt` to install the requirments needed to run our application. 

3. To run the following tests: 
- `cd \app\GroupFormer`
 - `python manage.py test projects` will run tests on the projects Django app.
 - `python manage.py test setup_screen`
 NOTE for running tests: You need to download the selenium webdriver and put it in your PATH variable.

 Download: https://chromedriver.chromium.org/downloads
 Make sure this matches your chrome version
 Update PATH Environment Variable:
 Windows:
 Save chromedriver.exe to a path such as C:\Program Files\Selenium
 Press the windows button and search 'advanced system settings'
 Click 'Environment Variables'
 Edit your User or System PATH variable adding the directory you chose
 Further Note: Currently an issue with Chrome v89 that will be fixed in v90 but is currently in beta.
 Selenium will spew some warning messages, but this doesn't effect the integration tests aside from
 clogging the terminal output.
 https://stackoverflow.com/questions/65080685/usb-usb-device-handle-win-cc1020-failed-to-read-descriptor-from-node-connectio

 The WebDriver used for the Selenium test is geckodriver, a Firefox webdriver.
 Tester must have Firefox installed and install the geckodriver executable and include its path on the system PATH to test.
 To test the response_screen endpoint:
 - `python manage.py test min_iteration2.tests.MinIteration2ResponseScreenTests`
 To test the groupformer_list endpoint:
 - `python manage.py test min_iteration2.tests.SeleniumGroupformerList`
 https://github.com/mozilla/geckodriver/releases
 
 - `python manage.py test dbtools` will test the database. 

4. After running  you can look at the output in localhost:8000 in your browser by running the following commands 
 - `python manage.py runserver` will run the server on localhost at port 8000.
