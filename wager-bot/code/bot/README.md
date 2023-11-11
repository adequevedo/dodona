# Bot 


## Docker 

docker build -t wager-bot .

gcloud auth application-default login

docker run -p 8080:8080 -v ~/.config:/root/.config wager-bot