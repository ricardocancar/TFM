#!/bin/bash
source /home/ricardo/anaconda3/bin/activate TFM_env
systemctl start docker

#docker start -ai speaker-recognitionInstance
# docker start -ai 9a5076499040 
#If you want to attach the container and drop to a shell, you can use:
### docker exec -it my_container /bin/bash

docker start   93a255fe35f7 # 03ee6f3baad4
docker start   9a5076499040

dir="host$2"
docker exec -ti 9a5076499040 python /proto-speaker-recognition/speaker-recognition/split_audio.py -i $1 -o "/host/home/ricardo/Documents/TFM/codigo/predict/"

docker exec -it 93a255fe35f7 python root/speaker-recognition/src/speaker-recognition.py -t predict -i "/host/home/ricardo/Documents/TFM/codigo/predict/*.wav" -c $2 -m root/speaker-recognition/src/model.out

docker exec -ti 9a5076499040 python /proto-speaker-recognition/speaker-recognition/order_prediction.py -i $1 -c $dir

rm -r "$dir/predict/*.wav"
# rm -r predictions.csv
rm -r "$dir/audio_to_txt/*.wav"

