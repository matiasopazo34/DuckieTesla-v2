#!/usr/bin/env python3
import rospy #importar ros para python
from std_msgs.msg import String, Int32 #importa mensajes de ROS tipo String y Int32
import cv2 # importar libreria opencv
import os
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
from cv_bridge import CvBridge # importar convertidor de formato de imagenes

from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage, Image, Joy
from duckietown_msgs.msg import WheelsCmdStamped

class Template(DTROS):
    def __init__(self, node_name):
        super(Template, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        vehicle_name = os.environ['VEHICLE_NAME']
        self._joy = f"/{vehicle_name}/joy"
        self.sub = rospy.Subscriber(self._joy , Joy, self.callback)
        #publicar la intrucciones del control en possible_cmd
        # self.publi = rospy.Publisher("/duckiebot/wheels_driver_node/car_cmd", Twist2DStamped, queue_size = "x")
        # self.twist = Twist2DStamped()
        self.i = 1


    def callback(self,msg):
        avanzar = msg.axes[0]
        #lo que hara este if sera provocar que las ruedas vayan
        #en sentidos opuestos cuando desee girar, es decir,
        #al pulsar la tecla para girar a la derecha, una de las ruedas
        #girara en sentido horario y la otra en sentido anti-horario
        if msg.axes[1]>=0:
            left=msg.axes[1]
            right=-msg.axes[1]
        elif msg.axes[1]<0:
            left=-msg.axes[1]
            right=msg.axes[1]
        velocidad = str(str(avanzar)+","+str(left)+","+str(right))
        direction = "/code/vel.txt" #aqui esta el absolute
        if self.i == 1:
        	velocidades = open(direction, "x")
        	velocidades.close()
        	velocidades = open(direction, "w")
        	velocidades.write(velocidad+"\n")
        else:
        	velocidades = open(direction, "a")
        	velocidades.write(velocidad+"\n")
        	velocidades.close()
        self.i += 1

if __name__ =='__main__':
    node = Template(node_name='template_node') # creacion del nodo
    #keep spinning
    rospy.spin()

#codigo viejo

    #def publicar(self, msg):
        #self.publi.publish(msg)

        # avanzar = msg.axes[2] #r2
        # giro = msg.axes [0]
        # z = msg.axes[]

        #print(freno, y, x)
        #self.twist.omega = 0
        #self.twist.v = 0

        # self.publi.publish(self.twist) #mensaje que se publica, luego el duckie lo recibe


#mensaje que se publica, luego el duckie lo recibe

# def main():
#     rospy.init_node('test') #creacion y registro del nodo!

#     obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

#     #objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

#     rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers
