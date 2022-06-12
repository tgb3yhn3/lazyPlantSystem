from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import numpy as np
from numpy import interp  # To scale values
from flask import Flask, render_template, Response
import cv2
import _thread
import time
import pymysql
 # To communicate with SPI devices
import datetime
from dbutils.pooled_db import PooledDB

# import spidev
# import RPi.GPIO as GPIO
# import adafruit_dht
# DHT_PIN=16
# PWM_PIN=20
# DIR_PIN=21
# LED_PIN=1
# BUTTON_PIN=7
# MOTOR_RELAY_PIN=12


# RELAY_ON=False
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)#use BCM mode
# GPIO.setup(PWM_PIN, GPIO.OUT)
# GPIO.setup(DIR_PIN, GPIO.OUT)
# GPIO.setup(MOTOR_RELAY_PIN, GPIO.OUT)
# GPIO.setup(LED_PIN, GPIO.OUT)
# GPIO.setup(BUTTON_PIN, GPIO.IN)
# device=adafruit_dht.DHT11(DHT_PIN)

# pwmOut = GPIO.PWM(PWM_PIN, 50)#inA control Fan speed
# GPIO.output(DIR_PIN,False)#inB control fan direction
# spi = spidev.SpiDev() # Created an object
# spi.open(0,0) 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '51689883'
app.config['MYSQL_DB'] = 'sensordata'
my=MySQL(app)
mysql = PooledDB(pymysql,10,host='localhost',user='root',passwd='51689883',db='sensordata',port=3306,autocommit=True) #5為連線池裡的最少連線數
# pool = MySQL(app)
camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
successRes={"status":"success"}

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/resetDB')
def reset():
    cur = mysql.connection().cursor()
    cur.execute('''
    DROP TABLE IF EXISTS `sensor`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor` (
  `no` int NOT NULL AUTO_INCREMENT,
  `humidity` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `temperature` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `soilHumidity` varchar(45) COLLATE utf8mb4_bin DEFAULT 'CURRENT_TIMESTAMP',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='for IOTclass';
ALTER TABLE sensor AUTO_INCREMENT = 1;
''')
    return "<h1>resetOK</h1>"
@app.route('/', methods=["POST","GET"])
@app.route('/home', methods=["POST","GET"])
def users():
    if request.method == "GET":
        cur = mysql.connection().cursor()
        # cur.execute(' INSERT INTO sensor VALUES (NULL, 97, 26,0,CURRENT_TIMESTAMP);')
        # mysql.connection().commit()
        cur.execute('''select * from sensor order by time DESC Limit 10;''')
        rv = cur.fetchall()

        # cur.execute(' INSERT INTO event VALUES (NULL, "澆水",CURRENT_TIMESTAMP);')
        # mysql.connection().commit()
        cur.execute('''select * from event order by time DESC Limit 10;''')
        ev = cur.fetchall()
        redata=[]
        time=[]
        for j in range(4):
            tmpdata=[]
            for i in rv:
                tmpdata.append(i[j+1])
            redata.append(tmpdata)
            
        # print(redata)
        return render_template("home.html",data=redata,rv=rv,ev=ev)
    if request.method=="POST":
        print(request.form)
        cur = mysql.connection().cursor()
        # print('''
        # select * from sensor where time between 
        # CONVERT(" '''+request.form['startdate']+' '+request.form['starttime']+':00'+''' ", DATETIME)
        # and CONVERT(" '''+request.form['enddate']+' '+request.form['endtime']+':00'+''' ",DATETIME);
        # ''')
        cur.execute('''
        select * from sensor where time between 
        CONVERT(" '''+request.form['startdate']+' '+request.form['starttime']+':00'+''' " ,DATETIME)
        and CONVERT(" '''+request.form['enddate']+' '+request.form['endtime']+':00'+''' ",DATETIME) order by time DESC;
        ''')
        
        rv = cur.fetchall()
        cur.execute('''
        select * from sensor where time between 
        CONVERT(" '''+request.form['startdate']+' '+request.form['starttime']+':00'+''' " ,DATETIME)
        and CONVERT(" '''+request.form['enddate']+' '+request.form['endtime']+':00'+''' ",DATETIME) order by time DESC;
        ''')
        ev = cur.fetchall()
        redata=[]
        time=[]
        for j in range(4):
            tmpdata=[]
            for i in rv:
                tmpdata.append(i[j+1])
            redata.append(tmpdata)
            
        # print(redata)
        return render_template("home.html",data=redata,rv=rv,ev=ev)
@app.route('/qset',methods=["GET","POST"])
def quickset():
    if request.method == "GET":
        cur=mysql.connection().cursor()
        cur.execute(' select * from targetPlant;')
        rv = cur.fetchall()
        plant=[]
        for i in rv:
            print(i[1])
            plant.append(i[1])
        print(plant)
        return render_template("quicksetting.html",rv=rv)
    if request.method == "POST":
        cur=mysql.connection().cursor()
        cur.execute('insert into targetPlant values('+
        'NULL,"'+
        request.form['name']+'",'+
        request.form['temp']+' , '+
        request.form['humi']+' , '+
        request.form['light']+' , '+
        request.form['soil']+'  '+  
           ' );')
           
        cur.execute(' select * from targetPlant;')
        rv = cur.fetchall()
        plant=[]
        for i in rv:
            print(i[1])
            plant.append(i[1])
        print(plant)
        return render_template("quicksetting.html",rv=rv)
@app.route('/set' ,methods=["POST","GET"])
def setting():
     if request.method == "GET":
        cur = mysql.connection().cursor()
        cur.execute(' select * from target;')
        rv = cur.fetchone()
        
        return render_template("setting.html",rv=rv)
     if request.method == "POST":
        cur = mysql.connection().cursor()
        print(" UPDATE target SET temp="+request.form['targetTemp']+" , humi="+request.form['targetHumi']+" , light="+request.form['targetLight']+" , soil="+request.form['targetSoil']+" where no=1;")
        cur.execute(" UPDATE target SET temp="+request.form['targetTemp']+" , humi="+request.form['targetHumi']+" , light="+request.form['targetLight']+" , soil="+request.form['targetSoil']+" where no=1;")
        mysql.connection().commit()
        cur.execute(' select * from target ;')
        rv = cur.fetchone()
        
        return render_template("setting.html",rv=rv)
@app.route('/set/<string:setplant>' ,methods=["POST","GET"])
def setplant(setplant):
    if request.method == "GET":
        cur = mysql.connection().cursor()
        cur.execute("select * from targetPlant where name='"+setplant+"';")
        rv=cur.fetchone()
        cur.execute(" UPDATE target SET temp="+str(rv[2])+
        " , humi="+str(rv[3])+
        " , light="+str(rv[4])+
        " , soil="+str(rv[5])+
        " , plant='"+str(rv[1])+
        "'  where no=1;"
        )
        mysql.connection().commit()
        
        return setting()
@app.route('/readJson' )
def readJson():
    import json
    with open('plants.json', newline='' ,encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)
        # 或者這樣
        # data = json.loads(jsonfile.read())
        for i in data['plants']:
            print(i['name'])
            print(i['temp'])
            print(i['humid'])
            print(i['lightTime'])
            print(i['soilHumid'])
            cur = mysql.connection().cursor()
            cur.execute("insert INTO targetPlant VALUES(NULL,'"+i["name"]+"',"+i['temp']+","+i['humid']+","+i['lightTime']+","+i['soilHumid']+");")
# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def rasberrypi():
   
    #setup
    #-----------------

    while True:
        try:
            cur.execute('select * from target')
            rv = cur.fetchone()

            targetTemp=rv[1]
            targetHumi=rv[2]
            targetLight=rv[3]
            targetSoil=rv[4]
            t=device.temperature
            h=device.humidity
            if(t>=targetTemp or h>targetHumi):
                pwmOut.start(50)
            else:
                pwmOut.stop(0)
            tonow = datetime.datetime.now()
            
            dts = str(tonow.year)+str(tonow.month)+str(tonow.day)
            dt = datetime.datetime.strptime(dts,"%Y%m%d")
            delta=datetime.timedelta(hours=targetLight)
            local=datetime.timedelta(hours=8)
            now=local+datetime.datetime.now()#實際時間
            target=dt+local+delta
            if(now<target):
                GPIO.output(LED_PIN,True)
                print("LED ON")
            else:
                GPIO.output(LED_PIN,False)
                print("LED OFF")
            print(t)
            print(h)

            s = analogInput(0) # Reading from CH0
            s = interp(s, [0, 1023], [100, 0])
            s = int(s)
            print("Moisture:", s)
            nows=100-s
            if(nows<targetSoil):
                GPIO.output(MOTOR_RELAY_PIN,True)
            else:
                GPIO.output(MOTOR_RELAY_PIN,False)
            cur = mysql.connection().cursor()
            cur.execute(' INSERT INTO sensor VALUES (NULL, '+str(h)+', '+str(t)+','+str(s)+',CURRENT_TIMESTAMP);')
            mysql.connection().commit()
            time.sleep(60)
        except KeyboardInterrupt:
            device.exit()
            GPIO.output(MOTOR_RELAY_PIN,False)
            GPIO.output(LED_PIN,False)
            pwmOut.stop(0)
            print("KI")
            break
        except RuntimeError:
            print("runtimeError retry 5 second later")
            time.sleep(10)
            continue
        except OverflowError:
            print("OverflowError retry 5 second later")
            time.sleep(10)
            continue
        
if __name__ == '__main__':
   # _thread.start_new_thread ( rasberrypi,() )
    app.run('0.0.0.0',debug=True)
    
   