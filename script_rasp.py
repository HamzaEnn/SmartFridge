# Importing library
import cv2
from pyzbar.pyzbar import decode

import mysql.connector
from mysql.connector.constants import ClientFlag
import sqlalchemy

#For the ultrasonor sensor
import RPi.GPIO as GPIO
import time
#api to get barcode from image
import cv2
from pyzbar.pyzbar import decode

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins : For sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#Configuration for the database
config = {
    'user': 'root',
    'password': 'pi1234',
    'host': '34.155.207.12'
}

# now we establish our connection
print("connecting to database...")
config['database'] = 'testdb'  # add new database to config dict
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()
print("connected.")

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
  
# Make one method to decode the barcode
def BarcodeReader(image):
     
    # read the image in numpy array using cv2
    img = cv2.imread(image)
      
    # Decode the barcode image
    detectedBarcodes = decode(img)
      
    # If not detected then print the message
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:
       
          # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes: 
           
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect
             
            # Put the rectangle in image using
            # cv2 to highlight the barcode
            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10),
                          (255, 0, 0), 2)
             
            if barcode.data!="":
                
                # cv2.imshow("Image", img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
               
                # Print the barcode data
                #print(barcode.data)
                #print(barcode.type)
                return (barcode.data)

def send_barcode_server(barcode) :
    query = ("INSERT INTO barcodes (user, code) "
             "VALUES ('gdai', "+barcode+" )")
    cursor.execute(query)
    cnxn.commit()
    
if __name__ == "__main__":
    
    ready = False
    i = 1
    distance_max = 15
    distance_min = 5
    
    try:
        while True:
            dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            if (dist > distance_max) :
                ready = True
            elif dist >= distance_min and dist <= distance_max and ready :
                print("calling the api to get the barcode number")
                image = "./product"+str(i)+".jpg"
                barcode = BarcodeReader(image).decode("utf-8") 
                if (barcode) :
                    print(barcode)
                    send_barcode_server(barcode)
                    print("barcode sent to database")
                    ready = False
                    i = (i % 2) + 1
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()