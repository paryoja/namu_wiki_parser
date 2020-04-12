from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{"host": "192.168.29.196", "port": 9200}])

body = {
    "settings": {  # 색인(index) 정의
        "number_of_shards": 1,  # 샤드 개수
        "number_of_replicas": 0,  # 레플리카 개수
        "index": {  # 색인 전체 설정
            "analysis": {
                "analyzer": {
                    "nori_analyzer": {  # 사용자 정의 분석기
                        "type": "custom",
                        "tokenizer": "nori_user_dict",  # 토크나이저 설정
                        "filter": ["my_posfilter"],
                    }
                },
                "tokenizer": {
                    "nori_user_dict": {  # 토크나이저 정의
                        "type": "nori_tokenizer",  # 한글 분석기 (nori)
                        "decompound_mode": "mixed",
                        # 토큰을 처리하는 방법, 분해하지 않는다(none), 분해하고 원본삭제(discard), 분해하고 원본 유지(mixed)
                        # "user_dictionary": "userdict_ko.txt",
                    }
                },
                "filter": {
                    "my_posfilter": {  # 제거 할 불용어들
                        "type": "nori_part_of_speech",
                        "stoptags": [
                            "E",
                            "IC",
                            "J",
                            "MAG",
                            "MAJ",
                            "MM",
                            "SP",
                            "SSC",
                            "SSO",
                            "SC",
                            "SE",
                            "XPN",
                            "XSA",
                            "XSN",
                            "XSV",
                            "UNA",
                            "NA",
                            "VSV",
                        ],
                    }
                },
            }
        },
    },
    "mappings": {
        "doc": {
            "properties": {
                "title": {"type": "text", "analyzer": "nori_analyzer"},  # 제목
                "text": {"type": "text", "analyzer": "nori_analyzer"},  # 글 내용
            }
        }
    },
}

res = es.indices.create(index="namu_wiki_analysis", body=body, include_type_name=True)
