FROM elasticsearch:7.6.0
MAINTAINER Yoonjae Park <yj0604.park@gmail.com>

COPY ./config/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
COPY ./entry/es_entry.sh /usr/local/bin/es_entry.sh

RUN bin/elasticsearch-plugin install analysis-nori
RUN chmod u+x /usr/local/bin/es_entry.sh

ENTRYPOINT ["/usr/local/bin/es_entry.sh"]
