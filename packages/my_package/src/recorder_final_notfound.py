#!/usr/bin/env python3
import rospy #importar ros para python
from std_msgs.msg import String, Int32 #importa mensajes de ROS tipo String y Int32
import cv2 # importar libreria opencv
import os
# from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
from cv_bridge import CvBridge # importar convertidor de formato de imagenes

import message_filters
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage, Image, Joy
from duckietown_msgs.msg import WheelsCmdStamped


#rospy.init_node('TemplateNode')
#variable self.i += 1


def tomar_img(camera_sub, joy_sub, i=0):
	bridge = CvBridge()
	rate = rospy.Rate(10)
	# CAPTURA DE IMAGENES, aqui y siempre se usará el directorio /code
	image = bridge.compressed_imgmsg_to_cv2(camera_sub, "bgr8")
	directorio =r'/code/'
	#Se escribe la imagen en la carpeta del path
	os.chdir(directorio)
	nombre = "imagen"+str(i)+".jpg"
	nombre_path = r"/code/"+"imagen"+str(i)+".jpg"
	print("Before saving image:")
	print(os.listdir(directorio))
	#aqui se graba la imagen
	cv2.imwrite(nombre, imagen) #luego se puede procesar la imagen
	print("la imagen "+str(nombre)+" se guardó bien uwu")

	#CAPTURA DE VELOCIDADES
	avanzar = joy_sub.axes[0]
	if joy_sub.axes[1]>=0:
		left=joy_sub.axes[1]
		right=-joy_sub.axes[1]
	elif msg.axes[1]<0:
		left=-joy_sub.axes[1]
		right=joy_sub.axes[1]
	velocidad = str(str(avanzar)+","+str(left)+","+str(right))
	direction = "/code/vel.txt" #aqui esta el absolute
	if i == 1:
		velocidades = open(direction, "x")
		velocidades.close()
		velocidades = open(direction, "w")
		velocidades.write(velocidad+"\n")
		velocidades.close()
	else:
		velocidades = open(direction, "a")
		velocidades.write(velocidad+"\n")
		velocidades.close()
	print("la velocidad es :"+velocidad)
	i+=1


vehicle_name = os.environ['VEHICLE_NAME']
camera_topic = f"/{vehicle_name}/camera_node/image/compressed"
joy_topic = f"/{vehicle_name}/joy"
camera_sub = message_filters.Subscriber(camera_topic, CompressedImage)
joy_sub = message_filters.Subscriber(joy_topic, Joy)
dts = message_filters.ApproximateTimeSynchronizer([camera_sub, joy_sub], queue_size=5, slop=0.1)
dts.registerCallback(tomar_img)

rospy.spin()

