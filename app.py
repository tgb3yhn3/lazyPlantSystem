from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import numpy as np
from flask import Flask, render_template, Response
import cv2
import _thread
import time
import pymysql
from dbutils.pooled_db import PooledDB
# import adafruit_dht
# import spidev # To communicate with SPI devices
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

@app.route('/set' ,methods=["POST","GET"])
def setting():
     if request.method == "GET":
        cur = mysql.connection().cursor()
        cur.execute(' select * from target;')
        rv = cur.fetchone()
        cur.execute(' select * from targetPlant;')
        rvplant = cur.fetchall()
        print(rvplant)
        plant=[]
        for i in rvplant:
            print(i[1])
            plant.append(i[1])
        return render_template("setting.html",rv=rv,rvplant=plant)
     if request.method == "POST":
        cur = mysql.connection().cursor()
        print(" UPDATE target SET temp="+request.form['targetTemp']+" , humi="+request.form['targetHumi']+" , light="+request.form['targetLight']+" , soil="+request.form['targetSoil']+" where no=1;")
        cur.execute(" UPDATE target SET temp="+request.form['targetTemp']+" , humi="+request.form['targetHumi']+" , light="+request.form['targetLight']+" , soil="+request.form['targetSoil']+" where no=1;")
        mysql.connection().commit()
        cur.execute(' select * from target ;')
        rv = cur.fetchone()
        return render_template("setting.html",rv=rv)
def rasberrypi():
    # DHT_PIN=16
    # PWM_PIN=20
    # DIR_PIN=21
    # LED_PIN=1
    # BUTTON_PIN=7
    # MOTOR_RELAY_PIN=12
    # targetTemp=25
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
    # #setup
    #-----------------

    while True:
        
        cur = mysql.connection().cursor()
        cur.execute(' INSERT INTO sensor VALUES (NULL, 1,2,3,CURRENT_TIMESTAMP);')
        mysql.connection().commit()
        print("ya")
        time.sleep(10)
          
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
            mysql.connection().commit()
if __name__ == '__main__':
    _thread.start_new_thread ( rasberrypi,() )
    app.run(debug=True)
   