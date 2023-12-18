#!/usr/bin/env python3
import numpy as np
import cv2
import os
import tensorflow as tf
import rospy #importar ros para python
from std_msgs.msg import String, Int32 #importa mensajes de ROS tipo String y Int32
from sensor_msgs.msg import Joy # impor mensaje tipo Joy
from geometry_msgs.msg import Twist, Point # importar mensajes de ROS tipo geometry / Twist
from duckietown_msgs.msg import Twist2DStamped 
import cv2 # importar libreria opencv
from cv_bridge import CvBridge # importar convertidor de formato de imagenes
import message_filters
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage, Image, Joy
from duckietown_msgs.msg import WheelsCmdStamped

path = '/code'
#Se tiene modelo de prueba por defecto en carpeta models
#Se ejecuta el modelo de red neuronal

class TemplateNode(DTROS):
    def __init__(self, node_name):
        super(TemplateNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        vehicle_name = os.environ['VEHICLE_NAME'] 
        self._camera_topic = f"/{vehicle_name}/camera_node/image/compressed"
        #publicar la intrucciones del control en possible_cmd
        self._wheels_topic=f"/{vehicle_name}/wheels_driver_node/wheels_cmd"
        self._publisher = rospy.Publisher(self._wheels_topic, WheelsCmdStamped, queue_size=1)
        self.pub_pos = rospy.Publisher("/duckiebot/smart", Point, queue_size = 1) 
        self.twist = Twist2DStamped()
        self.model = tf.keras.models.load_model(os.path.join(path,"models", "modeloco.h5"),compile=False)
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    """   
    def check_tensorflow_gpu(self, context: Context):
        #import tensorflow as tf
        name = tf.test.gpu_device_name()
        context.info(f"gpu_device_name: {name!r} ")
        if not name:
            no_hardware_GPU_available(context)
    """   

    def callback(self,msg):
        #context.info("Checking GPU availability...")
        limit_gpu_memory()
        #self.check_tensorflow_gpu(context)
        #se obtiene una imagen
        smart = Point()
        bridge = CvBridge()
        image = bridge.imgmsg_to_cv2(msg, "bgr8")
        # img = image[180:480, :, :]
        scale_percent = 25 # porcentaje de la imagen original
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        obs_ = np.expand_dims(resized,axis=0)
        _key = self.model.predict(obs_)
        print(_key)
        _key = np.argmax(_key[0])
        print(_key)
        if _key == 0:
            #pa delente
            self.twist.v = 0.4
            self.twist.omega = 0
            print("adelante")
            smart.x=_key
            self.publi.publish(self.twist)
        elif _key == 1:
            #pa la derecha
            self.twist.omega = -15
            self.twist.v = 0
            print("derecha")
            smart.x=_key
            self.publi.publish(self.twist)
        elif _key == 2:
            #pa la izquierda
            self.twist.omega = 1*10
        self.pub_pos.publish(smart)
        print("publicado")

def limit_gpu_memory(memory_limit: int = 1024):
    """Restricts TensorFlow to only allocated 1GB of memory on the first GPU"""
    #import tensorflow as tf
    physical_gpus = tf.config.experimental.list_physical_devices("GPU")
    if physical_gpus:
        try:
            c = [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory_limit)]
            tf.config.experimental.set_virtual_device_configuration(physical_gpus[0], c)
            logical_gpus = tf.config.experimental.list_logical_devices("GPU")
            logger.info(num_physical_gpus=len(physical_gpus), num_logical_gpus=len(logical_gpus))
        except RuntimeError as e:
            # Virtual devices must be set before GPUs have been initialized
            logger.error(e)      

if __name__ =='__main__':
    # create the node
    node = TemplateNode(node_name='template_node') # creacion del nodo
    # keep spinning
    rospy.spin()