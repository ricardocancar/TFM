docker pull qacollective/ppwwyyxx-speaker-recognition

docker run --name speaker-recognitionInstance -ti -v /:/host speaker-recognition

docker build -f Dockerfile -t speaker .

docker run --name speaker-instance -ti -v /:/host speaker

# docker run -v /var/run/docker.sock:/var/run/docker.sock -d --name 9dd3dee83407 ppwwyyxx-speaker-recognition

