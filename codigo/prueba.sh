#!/bin/bash
source /home/ricardo/anaconda3/bin/activate TFM_env
systemctl start docker
python3 split_audio.py -i $1 -o "./predict/"

#docker start -ai speaker-recognitionInstance

#If you want to attach the container and drop to a shell, you can use:
### docker exec -it my_container /bin/bash

docker start   93a255fe35f7 # 03ee6f3baad4
 
docker exec -it 93a255fe35f7 root/speaker-recognition/src/speaker-recognition.py -t predict -i "/host/home/ricardo/Documents/TFM/codigo/predict/*.wav" -m root/speaker-recognition/src/model.out
python3 order_prediction.py -i $1

chmod 666 "sorted_prediction.csv"

python3 au_texto.py -a /home/ricardo/Documents/TFM/codigo/audio_to_txt
# rm -r predict/*.wav
#python au_texto.py -a /home/ricardo/Documents/TFM/codigo/audio_to_txt/

# ffmpeg -i my_video.mp4 -ac 1 -ar 96000 output_audio.wav



