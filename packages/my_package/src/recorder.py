#!/usr/bin/env python3
import rospy #importar ros para python
from std_msgs.msg import String, Int32 #importa mensajes de ROS tipo String y Int32
import cv2 # importar libreria opencv
import os
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
from cv_bridge import CvBridge # importar convertidor de formato de imagenes

from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage, Image
from duckietown_msgs.msg import WheelsCmdStamped


class TemplateNode(DTROS):
	def __init__(self, node_name):
		super(TemplateNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
		vehicle_name = os.environ['VEHICLE_NAME']
		self._camera_topic = f"/{vehicle_name}/camera_node/image/compressed"
		self._bridge = CvBridge()
		# aqui configuramos el suscriber
		self.sub = rospy.Subscriber(self._camera_topic, CompressedImage, self.tomar_img)
		#lo antiguo está aqui
		#self.args = args
		# self.Sub_Cam = rospy.Subscriber("/db1/camera_node/image/compressed", Image, self.tomar_img)
		self.i = 0

	#def publicar(self, msg):
	#self.publi.publish(msg)

	def tomar_img(self, msg):
		rate = rospy.Rate(10)
		image = self._bridge.compressed_imgmsg_to_cv2(msg)
		# bridge = CvBridge()
		# image = bridge.imgmsg_to_cv2(msg, "bgr8")
		#Se declara la carpeta donde se guardaran las imagenes (crear en la misma ruta que se encuentra recorder.py)
		path = '/home/matiuwu/Escritorio/Laboratory juju/recorder1/packages/my_package'
		#Se escribe la imagen en la caperta del path
		nombre = "imagen"+str(self.i)+".jpg"
		cv2.imwrite(nombre, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
		#with open("text.txt","w") as file:
		#	file.write("I am learning Python!\n")
		#	file.write("I am really enjoying it!\n")
		#	file.write("And I want to add more lines to say how much I like it")
		print("la imagen "+str(nombre)+" se guardó bien uwu")
		self.i+=1
"""
def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers
"""

if __name__ =='__main__':
	# create the node
	node = TemplateNode(node_name='template_node') # creacion del nodo
	# keep spinning
	rospy.spin()
