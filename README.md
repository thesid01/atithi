# atithi
A ChatBot for Smart India Hackathon

#### How to get Started (USE LINUX)

````
Create a Virtual Environment
virtualenv -p python3 .
source bin/activate
pip install mindmeld
pip install mindmeld[bot]
docker pull mindmeldworkbench/duckling:master
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:6.7.0
sudo docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.7.0
docker run -p 0.0.0.0:7151:7151 mindmeldworkbench/duckling:master -ti -d
./load_kb.sh
python -m chatbot build
python -m chatbot converse
````
