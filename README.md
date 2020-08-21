# FavRip

FavRip is a python3.7+ tool built to asynchronously rip large amounts of Favicon's from websites.

# Usage

Clone
``` sh
git clone git@github.com:mikeshearer/favrip.git
```
Setup environment
``` sh
virtualenv --python=`which python3.7` favrip
source favrip/bin/activate
pip install -r requirements.txt
ulimit -S -n 4096 # Up your system's allowed number of open files
```
Create a sample file
``` sh
sudo yum install zip unzip # If centOS
sudo apt-get install zip unzip # If ubuntu
brew install zip unzip # if iOS
wget http://s3.amazonaws.com/alexa-static/top-1m.csv.zip -O temp.zip
unzip temp.zip && rm temp.zip

head -n 10000 top-1m.csv > top-10k.csv # Really any number you want
```

Run
``` sh
python -m favrip top-10k.csv --parallelism 200 --timeout 15
```