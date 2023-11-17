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


class TemplateNode(DTROS):
	def __init__(self, node_name):
		super(TemplateNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
		#configuración de topicos
		vehicle_name = os.environ['VEHICLE_NAME']
		self._camera_topic = f"/{vehicle_name}/camera_node/image/compressed"
		self._joy = f"/{vehicle_name}/joy"
		#configuracion suscriber y message filters
		camera_sub = message_filters.Subscriber(self._camera_topic, CompressedImage)
		joy_sub = message_filters.Subscriber(self._joy, Joy)
		# dts = message_filters.ApproximateTimeSynchronizer([camera_sub, joy_sub], queue_size=5, slop=0.1)
		# dts.registerCallback(tomar_img(self, camera_sub, joy_sub))
		#importar CvBridge
		self._bridge = CvBridge()
		dts = message_filters.ApproximateTimeSynchronizer([camera_sub, joy_sub], queue_size=5, slop=0.1)
		dts.registerCallback(self.tomar_img)
		# aqui configuramos el suscriber
		# self.sub = rospy.Subscriber(self._camera_topic, CompressedImage, self.tomar_img)
		# variable auxiliar
		self.i = 0

	def tomar_img(self, camera_sub, joy_sub): #cambiar las cosas por camera y joy
		rate = rospy.Rate(10)
		# CAPTURA DE IMAGENES, aqui y siempre se usará el directorio /code
		image = self._bridge.compressed_imgmsg_to_cv2(camera_sub, "bgr8")
		directorio =r'/code/'
		#Se escribe la imagen en la carpeta del path
		os.chdir(directorio)
		nombre = "imagen"+str(self.i)+".jpg"
		nombre_path = r"/code/"+"imagen"+str(self.i)+".jpg"
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
		if self.i == 1:
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
		self.i+=1

if __name__ =='__main__':
	# create the node
	node = TemplateNode(node_name='template_node') # creacion del nodo
	# keep spinning
	rospy.spin()
