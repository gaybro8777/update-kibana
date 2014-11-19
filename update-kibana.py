import json

from elasticsearch import Elasticsearch

ORIG_INDEX_PATTERN = "[logstash-]YYYY.MM.DD"
NEW_INDEX_PATTERN = ORIG_INDEX_PATTERN + ",[accounting-]YYYY.MM.DD"

def main():
    es = Elasticsearch()
    # query =
    dashboards = {}

    for hit in es.search(index="kibana-int", doc_type="dashboard", size=1000)["hits"]["hits"]:
        data = hit["_source"]
        dashboards[hit["_id"]] = hit["_source"]


    for id_, data in dashboards.items():
        dashboard = json.loads(data["dashboard"])

        # Here the modification takes place
        if dashboard["index"]["pattern"] == ORIG_INDEX_PATTERN:
            dashboard["index"]["pattern"] = NEW_INDEX_PATTERN

        dashboards[id_]["dashboard"] = json.dumps(dashboard)

    for id_, data in dashboards.items():
        es.delete(index="kibana-int", doc_type="dashboard", id=id_)
        es.create(index="kibana-int", doc_type="dashboard", id=id_, body=data)

if __name__ == "__main__":
    main()
