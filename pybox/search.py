import elasticsearch


class SimpleSearch(object):
    def __init__(self, index):
        self.es = elasticsearch.Elasticsearch()
        self.index = index

    def search(self, query, size=5):
        # single word query:
        # results = es.search(index=author, q=query, size=numResults)
        # phrase match query:
        results = self.es.search(
            index=self.index, body={"size": size, "query": {"match": {"content": {"query": query}}}}
        )
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
    print(search.search("conventional wisdom"))
