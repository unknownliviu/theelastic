import argparse
import elasticsearch


class SimpleSearch(object):
    def __init__(self, index):
        self.es = elasticsearch.Elasticsearch()
        self.index = index

    def search(self, query, size=5):
        # single word query:
        # results = es.search(index=author, q=query, size=numResults)
        # phrase match query:
        # queryjson = {"match": {"content": {"query": query}}}
        queryjson2 = {"match_phrase": {"content": {"query": query}}}
        results = self.es.search(index=self.index, body={"size": size, "query": queryjson2})
        hit_count = len(results["hits"]["hits"])
        if hit_count > 0:
            return self.__pretty(results)
        else:
            print("No results found")

    def __pretty(self, results):
        return {
            "count": results["hits"]["total"]["value"],
            "hits": [{"id": x["_id"], "data": x["_source"]} for x in results["hits"]["hits"]],
        }


if __name__ == "__main__":
    search = SimpleSearch("html")
    parser = argparse.ArgumentParser(description="SimpleSearch")
    parser.add_argument("--q", dest="query", type=str, help="query", required=True)
    parser.add_argument("--l", dest="limit", default=5, type=int, help="Max no of results")

    args = parser.parse_args()
    print(search.search(args.query, args.limit))
