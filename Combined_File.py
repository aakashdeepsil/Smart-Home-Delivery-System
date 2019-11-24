import boto3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from botocore.exceptions import ClientError
from test import RFID_CLASS
from process import Predictor
from ultrasonic_sensor import Ultrasonic
#from pirSensor import PIR

class smartDelivery:
    
    def __init__(self):
        #GPIO.setmode(GPIO.BCM)
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = self.dynamodb.Table('Customer_1')
        self.response = self.table.scan()
        self.data = self.response['Items']
        self.rfidObject = RFID_CLASS()
        self.predictObject = Predictor()
        #self.pirObject = PIR()
        self.ultrasonicObject = Ultrasonic()

    def recieveOrder(self):
        self.orderRecieved=False
        for self.dic in self.data:
            
            if int(self.dic["Status"])==0:
                print("Show rfid")
                if self.rfidObject.rfid_read():
                    self.orderRecieved=True
                    self.cameraDetection()


    def cameraDetection(self):
        if self.ultrasonicObject.ultra():
            self.prediction=self.predictObject.predictFace()
            if self.prediction==13:
                print("Done")
                self.sendEmailAlert()
                    
            elif self.prediction==1 or self.prediction==2 or self.prediction==0:
                print("Door Unlock")
    
            elif self.prediction==None:
                self.cameraDetection()
                

    def sendEmailAlert(self):
        SENDER = "adityak1277@gmail.com"
        RECIPIENT = str(self.dic["Email"])
                        
                    
        AWS_REGION = "us-west-2"

                   
        SUBJECT = "Alert!!"

                    
        BODY_TEXT = ("Unknown user tried to access your parcel!!! ")

        x=str(self.dic["orderID"])            
                    
        BODY_HTML = """<html>
                    <head></head>
                    <body>
                    <h1>Alert Message:</h1>
                    <p>Unknown user tried to access your parcel!!!</p>
                    </body>
                    </html>
                    """
                    
        CHARSET = "UTF-8"

                   
        client = boto3.client('ses',region_name=AWS_REGION)

                   
        try:
            response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                                ],
                                },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                            },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                            },
                        },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                                },
                    },
            Source=SENDER,
                            )
             
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
 
exam=smartDelivery()
exam.recieveOrder()
  
  