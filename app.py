from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import numpy as np
from flask import Flask, render_template, Response
import cv2

import time

app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '51689883'
app.config['MYSQL_DB'] = 'sensordata'
 
mysql = MySQL(app)
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
    cur = mysql.connection.cursor()
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
        cur = mysql.connection.cursor()
        cur.execute(' INSERT INTO sensor VALUES (NULL, 97, 26,0,CURRENT_TIMESTAMP);')
        cur.execute('''select * from sensor;''')
        mysql.connection.commit()
        rv = cur.fetchall()
        redata=[]
        time=[]
        for j in range(4):
            tmpdata=[]
            for i in rv:
                tmpdata.append(i[j+1])
            redata.append(tmpdata)
            
        # print(redata)
        return render_template("home.html",data=redata,rv=rv)
    if request.method=="POST":
        print(request.form)
        cur = mysql.connection.cursor()
        print('''
        select * from sensor where time between 
        CONVERT(" '''+request.form['startdate']+' '+request.form['starttime']+':00'+''' ", DATETIME)
        and CONVERT(" '''+request.form['enddate']+' '+request.form['endtime']+':00'+''' ",DATETIME);
        ''')
        cur.execute('''
        select * from sensor where time between 
        CONVERT(" '''+request.form['startdate']+' '+request.form['starttime']+':00'+''' " ,DATETIME)
        and CONVERT(" '''+request.form['enddate']+' '+request.form['endtime']+':00'+''' ",DATETIME);
        ''')
        
        rv = cur.fetchall()
        redata=[]
        time=[]
        for j in range(4):
            tmpdata=[]
            for i in rv:
                tmpdata.append(i[j+1])
            redata.append(tmpdata)
            
        # print(redata)
        return render_template("home.html",data=redata,rv=rv)

@app.route('/set')
def setting():
    return render_template("setting.html")
if __name__ == '__main__':
    app.run(debug=True)