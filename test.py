import boto3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from botocore.exceptions import ClientError

class RFID_CLASS:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.reader = SimpleMFRC522()
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        
    
    def rfid_read(self):
        while True:
            try:
                self.id, self.text = self.reader.read()
                #print(id)
                #print(text)
                if self.send_email():
                    return 1
            finally:
                #GPIO.cleanup()
                pass
                
    def send_email(self):
        table = self.dynamodb.Table('Customer_1')

        response = table.scan()
        data = response['Items']
        
        #print(data)

        orderid = int(self.text)
        rfid = self.id
                
        for dic in data:
            if rfid == dic["rfID"] and orderid == dic["orderID"] :
                print("Nice")
                SENDER = "adityak1277@gmail.com"
                RECIPIENT = str(dic["Email"])
                        
                    
                AWS_REGION = "us-west-2"

                    
                SUBJECT = "Order Status"

                    
                BODY_TEXT = ("Your order with id: "+ str(dic["orderID"]) + " has been delivered.")

                x=str(dic["orderID"])            
                    
                BODY_HTML = """<html>
                    <head></head>
                    <body>
                    <h1>Oder Status:</h1>
                    <p>Your order with id:{}has been delivered.</p>
                    </body>
                    </html>
                    """.format(x)
                    
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
                    print("Message sent.")
                    table.put_item(
                        Item={
                            'Customer_ID': 1,
                            'orderID': 4,
                            'rfID': 1002595244426,
                            'Email': "adityakumar.cs17@bmsce.ac.in",
                            'Status': 1,
                        }
                    )
                    return 1
                    #break
            else:
                print('Denied')
                return 0
