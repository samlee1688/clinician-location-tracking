from time import sleep
from shapely.geometry import Point, Polygon
import requests
import smtplib
import schedule

url=  "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/"
SENDER_EMAIL = "sammielee1688@gmail.com"
SENDER_APP_ID = "" # paste here
RECIPIENT_EMAIL = "coding-challenges+alerts@sprinterhealth.com"


def getStatus():
    print("run")
    for i in range(1,7):    # iterates through phlebotomists 1-6 (valid cases). Change loop to "for i in range(1,8):" for phlebotomist 7 (always out of range).
        response = requests.get(url+str(i))
        if response.status_code != 200:
            print("API Error: ", response.status_code)
            continue
        result = response.json()
        polygons = []
        point = None
        for obj in result['features']:
            if obj['geometry']['type']=="Point":
                if point is None: # prevent overwriting an existing point --> should not happen
                    point = obj['geometry']['coordinates']
            elif obj['geometry']['type']=='Polygon':
                polygons.append(obj['geometry']['coordinates'][0])  # list of zones for a phlebotomist (id:3 has multiple)
            else:
                print("unidentified type")        

        pointShapely = Point(point) # Converts all coordinates into Shapely objects
        polygonsShapely = []
        for polygon in polygons:
            polygonsShapely.append(Polygon(polygon))

        flag=False
        for polygon in polygonsShapely:
            if pointShapely.within(polygon) or pointShapely.touches(polygon):   # checks if phlebotomist is in any of the valid zones.
                flag=True
                break
        if not flag:
            #send email
            #print(f"point {i} is out of bounds")
            sendEmail(i)
    return True

def sendEmail(id: int):
    try:
        server = smtplib.SMTP("smtp.gmail.com")
        server.starttls()   # for secure connection (required)
        server.login(SENDER_EMAIL, SENDER_APP_ID)

        message = f"""
                    ALERT: Phlebotomist {id} is out of range!

                    From: Samuel Lee (sammielee1688@gmail.com)
                    """
        server.sendmail(SENDER_EMAIL,RECIPIENT_EMAIL, message)
    except Exception as e:
        print(e)


if __name__=='__main__':
    schedule.every(240).seconds.do(getStatus)    # adds a pending job of getStatus every 4 minutes
    getStatus() # initial call
    while True:
        schedule.run_pending() 
        sleep(1)    #buffer