# TFM

modulos de TFM.
![alt text](/diagrama/TFM.png)


### enviroment 

- python 3.6.5
  - [webrtcvad](https://github.com/wiseman/py-webrtcvad)==2.0.10
  - pandas==0.23.4
  - numpy==1.15.1
  - scipy==1.1.0
  - [speech_recognition](https://pypi.org/project/SpeechRecognition/)


Para el modelo de [speaker-recognition](https://github.com/ppwwyyxx/speaker-recognition) se uso el repositorio de https://github.com/ppwwyyxx/speaker-recognition el cual es realizado por medio de Gaussian Mixture Models. 

### Guia de installación de speaker-recognition.
Para simplificar el proceso de instalación del speaker-recognitions primero debemos instalar [docker](https://docs.docker.com/install/), una vez instalado docker procedemos a descargar la imagen docker del repositorio de **speaker-recognition**

    docker pull qacollective/ppwwyyxx-speaker-recognition

Esto nos ahorra muchos problemas de incompatibilidad. 

### uso de speaker recognition.
El speaker-recognition debe tener acceso a los directorios de nuestro ordenador, para ello usamos.

    sudo docker run --name speaker-recognitionInstance -ti -v /:/host speaker-recognition

Una vez hecho esto, entramos en el contenedor docker para entrenar el modelo.

    sudo docker start -ai speaker-recognitionInstance

copiamos el script speaker-recognition.py dentro del contenedor.

   sudo docker cp speaker-recognition.py speaker-recognitionInstance:/root/speaker-recognition/src/speaker-recognition.py

Procedemos a entrenar el modelo.

    cd /root/speaker-recognition/src/
    ./speaker-recognition.py -t enroll -i "/host/path/to/samples/label1 /host/path/to/samples/label2 " -m model.out

label1 y label2 serán las etiquetas las personas que queremos identificar.

Para rechazar muestras se debe entrenar un UBM, usando el comando de la siguiente forma logramos tener un UBM dentro de nuestro modelo UBM.

    ./speaker-recognition.py -t enroll -i "/host/path/to/samples/label1 /host/path/to/samples/label2 " -u "/host/path/to/samples/ubm" -m model.out

para clasificar las muestras dentro del modelo. 

    ./speaker-recognition.py -t enroll -i "/host/path/to/samples/label1 /host/path/to/samples/label2 " -m model.out

### prueba.sh 
este script de bash esta sujeto a cambios por ello el nombre.
antes de ejecutar este script se debe cambiar la líneas.

  docker start   container_id
 
  docker exec -it container_id root/speaker-recognition/src/speaker-recognition.py -t predict -i "/host/home/ricardo/Documents/TFM/codigo/   predict/*.wav" -m root/speaker-recognition/src/model.out

para saber la containder id que se generó tras hacer el pull de la imagen se usa el comando.

    sudo docker ps -aqf "name=speaker-recognitionInstance"

- q para que solo muestre el container id
- a para todos. funciona inclusive si no esta trabajando el contenedor
- f para filtrar

mode de ejecutar el script. 

    sudo bash prueba.sh /path/to/audio.wav

esto clasificara las muestras del audio indicado y si identifica algún sujeto capturara el fragmento de audio en el cual el sujeto identificado intervino y lo almacenara en la carpeta audio_to_txt.

pd. las muestras de entrenamiento y clasificación deben pasar por el mismo filtro. 
el script **split_audio.py** separa las muestras de audio cuando detecta silencio. además remueve las muestras que no detecta actividad de voz ya que las parte de silencio afectan negativamente la predicción del modelo. 

por lo que es importante que las muestras de audio que se van a entrenar pasen por este filtro antes de ser entrenadas y clasificadas por el speaker recognition.

los audios se descargan de [rtve](http://www.rtve.es/alacarta/videos/telediario/) en la pagina [descagatusvideos](http://www.descargavideos.tv/) los videos son descargados a formato mp4.

### Modulo 1:
Transforma el video a audio con las siguientes caracteristicas mono canal,
frecuencia de 16000 hz y formato .wav.

### Modulo 2:
Segmenta el audio, creando los puntos de cortes en las parte que el algoritmo detecta como silenciosas.

### Modulo 3:
Modelo de GMM de speaker recognition, que classifica el audio y genera como salida, un csv que indica tiempo de intervension dentro del telediario de los principales actores políticos de España y sus nombres.

### Modulo 4:
Toma la salida del modulo tres para cortar los segmentos de audio del audio original del telediario donde se identificó la participación de los principales actores políticos, según el speaker recognition. Luego los transforma a texto con la ayuda de la [API](https://pypi.org/project/SpeechRecognition/) de google.

### Modulo 5:
clasificacion de texto por completar.

### Modulo 6:
app del TFM por completar.
