FROM elasticsearch:7.6.0
MAINTAINER Yoonjae Park <yj0604.park@gmail.com>

COPY ./config/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]