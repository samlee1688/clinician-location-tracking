# Take Home Assessment: Clinician Location Tracking
By Samuel Lee

## Introduction
With mobile phlebotomists safety in mind, it is vital that we are tracking their locations to ensure they are in their expected locations. Here, this project aims to retrive the locations of all our Phlebotomists via API calls, validate if they are in their Polygon zone, and send an email alert to informed parties if not.

## Setup and Run Application
1: Please clone the repo into your local IDE.
2: Update global variable "SENDER_APP_ID" with a separately provided password.
NOTE: To use your own sender gmail account retrieve your personal APP ID via your settings in Google (Search "App Passwords"). Also update SENDER_EMAIL with new email.
3: Ensure Shapely is installed via pip install Shapely
4: Run python .\boundary_service.py


## Methods
### checkStatus():
Retrieves the current locations and bounded areas of the existing phlebotomists via an API call. Parses the GeoJSON data, checks if each Phlebotomist is in their respective area, and calls sendEmail() if not.
I/O: None, API url must be provided.

### sendEmail(id: int):
Establishes a connection to SMTP email server (a popular tool for python), drafts a custom message from SENDER_EMAIL to RECIPIENT_EMAIL indicating which phlebotomist is out of their zone.

### Main function code:
Sets checkStatus as a scheduled job. checkStatus() will be scheduled to run every 4 minutes.


## Notes
1: The 4 minute frequency was chosen as it is not necessary to always be checking every second (expensive + unlikely to move far in short intervals) but frequent enough such that informed users are still notified in time to take necessary protocols.
2:  Shapely is utilized to check if phlebotomists are in their respective areas. It is a simple tool that takes coordinate points to build points or a list of points to build a Polygon. Then, a couple calls will allow us to check if the point .touches() polygon or point .within() polygon.
3: A future consideration is to use async functions to check all phlebotomists concurrently, rather than iterate through a list of them. This may reduce checking time and handle phlebotomist errors better.


## Contact
For any questions or issues, please contact sammielee1688@gmail.com OR samuel.lee.syl27@yale.edu