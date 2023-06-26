#### Project Status: Incomplete.

# Project Title: Mail-correction API
## Project Description.
Mail correction API is an API written in Python capable of receiving an email address (correct/wrong), analyzing it to determine the issue with the email address before attempting to correct it and returning the corrected email to the user.

This system can be used to scan through your mailing list and instantly correct thousands of emails in order to reduce your bounce rate.

## How to use?
- Install all requirements in the requirements.txt file
- Navigate to the api folder in terminal
- Run the command: $ uvicorn main:app --reload
- Open: http://127.0.0.1:8000/docs in your browser or
- Open Postman and enter the url http://127.0.0.1:8000/basic-correction for basic correction attempts
- For more advanced email correction attempts, navigate to http://127.0.0.1:8000/advanced-correction
- Enter the email and process the post request.
