# atithi
A ChatBot for Smart India Hackathon

#### How to get Started (USE LINUX)
Install Docker

Create a Virtual Environment and activate it.
````
virtualenv -p python3 .
source bin/activate
````
Install dependencies
````
pip install mindmeld
pip install mindmeld[bot]
pip install -r requirements.txt
````
Pull docker images and start container
```
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:6.7.0
sudo docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.7.0
```
or
```
docker pull mindmeldworkbench/duckling:master
docker run -p 0.0.0.0:7151:7151 mindmeldworkbench/duckling:master -ti -d
```
start num-parse
```
mindmeld num-parse --start
```
Run SH file
````
run ./main.sh
````

