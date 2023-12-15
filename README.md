# DuckieTesla Reloaded

![Duckietown Engineering Chile](https://github.com/Felipeipe/bitacoras-2023/blob/main/img/duckietown_engineering_chile.png?raw=true)

## Introducción

Este es un proyecto que consiste en lograr la conducción autonoma de un duckiebot en las calles de DuckieTown. Dicho proyecto utiliza imitation learning cómo método, además de utilizar diverso software y hardware para ello. Se recomienda encarecidamente tener conocimientos acerca de ROS, dts y python. También se recomienda revisar la documentación oficial de DuckieTown. 

## Requisitos y Dependencias

### Hardware

- Robot Duckiebot Modelo DB21J  o similares correctamente configurado, este modelo incluye una tarjeta Nvidia Jetson Nano que se usará posteriormente. Para conseguir el Duckiebot y configurarlo correctamente se recomienda revisar el siguiente repositorio [repositorio oficial de duckietown](https://docs.duckietown.com/daffy/opmanual-duckiebot/intro.html)
- Pc con Ubuntu 20.04 instalado, con 40 GB de espacio libre extra, para los datos de entrenamiento. Además de ello debe tener las dependencias necesarias para ejecutar el proyecto, dichas dependencias se detallarán a continuación.
 
### Software e instalación de dependencias
Para ejecutar correctamente el proyecto se deben de tener todas las dependencias requeridas presentes en el repositorio de duckietown [repositorio oficial de duckietown](https://docs.duckietown.com/daffy/opmanual-duckiebot/intro.html) estas corresponden a:
- Docker
- Python 3
- DuckieTown Shell (dts)
  
Además de ello en el computador local se deben instalar las siguientes dependencias de python:
- ROS 1 - noetic
- Tensorflow
- OpenCV
- Matplotlib

#### Para la instalación de dependencias

En la terminal:

### Python3

```Bash
sudo apt update
sudo apt install python3
```

### Librerias de python3

```Bash
pip install tensorflow
pip install opencv-python
pip install matplotlib
```

### DTS

Para la instalación de Duckietown Shell, debe seguirse una serie de pasos para poder configurarlo correctamente. Debe seguir al pie de la letra [este tutorial](https://docs.duckietown.com/daffy/opmanual-duckiebot/setup/setup_laptop/setup_dependencies.html). Debes completar las secciones de [*laptop setup*](https://docs.duckietown.com/daffy/opmanual-duckiebot/setup/setup_laptop/index.html) y de [*accounts*](https://docs.duckietown.com/daffy/opmanual-duckiebot/setup/setup_account/index.html) para luego seguir el readme de [este repositorio](https://github.com/duckietown/duckietown-lx) hasta la sección 2.

Para poder flashear la sd, debes ejecutar este comando:

```Bash
dts init_sd_card --hostname <Nombre de duckie> --type duckiebot --configuration DB21J --wifi <WIFI>:<WIFI-password>
```

### ROS

Seguir [este tutorial](http://wiki.ros.org/noetic/Installation/Ubuntu). Si no sabes como modificar el archivo .bashrc, debes seguir [este otro tutorial](https://www.digitalocean.com/community/tutorials/bashrc-file-in-linux

## DuckieTesla v2
Se recomienda visitar la documentación Duckietown Developer Manual ya que el proyecto está construido tal cómo se detalla ahí, de esta manera le será más fácil comprender los pasos realizados, se puede revisar la documentación aqui [DuckieTown Developer Manual](https://docs.duckietown.com/daffy/devmanual-software/intro.html)

### PASO 0. Estructura del proyecto
En este caso, se desarrollaron todos los scripts necesarios dentro de este repositorio. Este se organiza de tal manera que en la carpeta "packages" se encuentran los scripts de python, estos serán ejecutados dentro del duckiebot utilizando dts. Además en la carpeta launchers se encuentran los lanzadores que ejecutan los scripts de packages. Por último en la carpeta entrenamiento se encuentran todas los archivos necesarios para llevar el entrenamiento a cabo, el modo de proceder se detallará a continuación. Nuevamente se recomienda visitar el repositorio Duckietown Developer puesto que ahí se detalla más acerca de esto.

El primer paso necesario es clonar el repositorio de este proyecto usando git clone. Luego de ello, dentro del directorio del proyecto se debe ejecutar 

```Bash
dts devel build -f
```
Esto crea el espacio de desarrollo para posteriormente utilizarlo en el duckiebot.

Por otro lado es necesario tener el duckiebot funcionando para ejecutar los respectivos scripts. Se puede comprobar su buen funcionamiento mediante

```Bash
dts fleet discover
```

### PASO 1. Recopilar datos de entrenamiento
Primero es necesario generar una base de datos para el entrenamiento, para ello se utilizará el script recorder_final.py, este mientras se ejecuta guarda en una carpeta imágenes de la cámara del duckiebot así como también un archivo de texto con las velocidades del duckiebot asociadas a cada imagen obtenida. Posteriormente estos datos se utilizan para entrenar la IA. Para ejecutar el recorder_final se debe lanzar el siguiente comando desde la computadora local:

```Bash
dts devel run -R Nombre_Duckiebot -L recorder-launch
```

Al ejecutarse, en la consola verá cómo se guardan las velocidades e imágenes. Al usar dts, en realidad se está ejecutando un container de docker, por lo que todos los archivos generados se guardarán en dicho container, es necesario rescatar y guardar estos datos, es decir, extraerlos desde el container. Para ello se genera un volumen dentro del computador local, por ello, es necesario ingresar a la carpeta del volumen, copiar y sacar los datos de allí puesto que después de ejecutar el script dichos datos se eliminarán, para ello se procede de la siguiente manera, con el script ejecutándose.

primero acceder al volumen mediante la terminal con permisos de administrador, para ello:
```Bash
sudo -i 
```
Luego acceder a la carpeta de volúmenes desde la terminal ejecutando:
```Bash
cd /var/lib/docker/volumes/
```
Aqui encontrará alguna carpeta con muchos carácteres como 278a767a8787c874845b8374e, esta carpeta es el volumen de docker, ingrese al directorio tal como
```Bash
cd 278a767a8787c874845b8374e
```
luego estando en el directorio es necesario copiarlo y pegarlo a algún directorio local de su computadora, para ello dentro del directorio ejecute
```Bash
cp -r /directorio_volumen/ /directorio_destino/
```
Es importante empezar y finalizar los directorios con "/" puesto que asi especificamos que son carpetas, asegúrese que el directorio local sea accesible, luego se usarán estos datos para el entrenamiento.
Con la carpeta con la base de datos creada se puede proseguir al siguiente paso.

### PASO 2. Generar modelo de la IA mediante el entrenamiento
Para este paso se utilizará sólo la carpeta /entrenamiento de este repositorio, todo esto no se ejecutará dentro del duckiebot, si no que en su computadora local para lograr entrenar la IA, tiene que tener en cuenta que se usan 6gb de ram aproximadamente en el entrenamiento, en caso de que su cpu no tenga dichas características, puede usar google colab con gpu activada.

Una vez con la carpeta anterioermente generada de datos es necesario exportarlos a la carpeta de /entrenamiento, en este caso todas las imágenes deben ser puestas en la carpeta /frames y el archivos de velocidades "vel.txt" dentro del directorio /entrenamiento, en el repositorio hay datos de muestra para guiar este proceso, estos datos de muestra sólo son de referencia, por favor eliminelos al momento de entrenar.

Una vez con los archivos colocados dirigirse a reader.py , modificar el path (si no se ha hecho aun) e indicar el número de datos que se quieren procesar en el entrenamiento, que son los datos obtenidos en el paso 1.

Luego se deben ejecutar los scripts que están dentro de /entrenamiento con una terminal desde dicha carpeta, primero el reader
```Bash
python3 reader.py 
```
Esto es solamente para asegurarse que los datos sean leídos.

Luego se utilizará neural.py, donde se encontrará la estructura de una red neuronal convolucional, la cual fue utilizada para procesar las imágenes asociadas a sus respectivas velocidades. Una capa de convolución es básicamente un preprocesamiento de los frames, haciéndolos pasar por filtros representados por matrices. Así, se aplica una operación matricial a cada mapa de características, generando nuevas imágenes alteradas que servirán para detectar patrones.

Luego dirigirse a neural.py y modificarlo, en este caso se debe especificar la ruta de guardado del modelo y su respectivo nombre dentro de las siguientes lineas de código
```Bash
96  #Se entrega dirección donde se guarda el modelo (modificar)
97  path = 'D:\ruta_para_guardar_modelo'
98  # Se corre el modelo con el conjunto de entrenamiento
99  #En este caso en particular no se uso un conjunto de validación exterior
100 name = 'nombre del modelo'
```
ahora se procede al entrenamiento, una vez ejecutándose dentro de la terminal se puede ver el progreso del entrenamiento con el archivo del modelo como resultado. Cuando termine de cargar, se verá el contador epoch 7/7 y un aviso de que el modelo ya esta listo. Ahora tendrá su modelo en la carpeta models listo para ser usado, para ello se utiliza el siguiente comando:
```Bash
python3 neural.py 
```
Una vez alcanzado este punto se habrá concluido el entrenamiento, con el archivo del modelo creado y por ende se puede proceder a la siguiente etapa.

### PASO 3. Implementación de la IA

Con el modelo creado, es necesario importar este a la carpeta /ENTRENAMIENTO/models, esto ya que es necesario importar el modelo a los containers de docker.
Una vez hecho esto nuevamente se debe ejecutar dts devel build -f para guardar los cambios.
```Bash
dts devel build -f
```
Por último, solamente se debe ejecutar el archivo autoduck.py para lograr el manejo autónomo del duckiebot, utilizando dts devel run de la siguiente manera
```Bash
dts devel run -R nombre_duckiebot -L autoduck-launch
```

Con esto el duckiebot debería recorrer perfectamente las calles de duckietown. Cabe decir que se debe modificar el repositorio en este último paso ya que esto no se ha podido probar con algún duckiebot, sin embargo se detallan las instrucciones para que grupos a futuro logren ejecutar este proyecto. Por último se dan agradecimientos a los proyectos anteriores que vienen desarrollando este proyecto, ya que son la base para lograr lo expuesto aquí.
