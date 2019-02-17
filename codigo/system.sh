#!/bin/bash
source /home/ricardo/anaconda3/bin/activate TFM_env
systemctl start docker


#docker start -ai speaker-recognitionInstance

#If you want to attach the container and drop to a shell, you can use:
### docker exec -it my_container /bin/bash

docker start   93a255fe35f7 # 03ee6f3baad4
for filename in "audio_start/.*wav"; do
    python3 split_audio.py 
    docker exec -it 93a255fe35f7 python root/speaker-recognition/src/speaker-recognition.py -t predict -m root/speaker-recognition/src/model.out
    python3 csv_to_sqlite.py
    python3 order_prediction.py

    python3 re_tests.py
    # rm predictions.csv
    # rm -r predict/*.wav
    # python au_texto.py -a /home/ricardo/Documents/TFM/codigo/audio_to_txt/

    # ffmpeg -i my_video.mp4 -ac 1 -ar 96000 output_audio.wavs
    rm -r predictions.csv
    rm -r predict/*.wav
    rm -r audio_to_txt/*.wav
    rm -r audio_start/*.wav
done
