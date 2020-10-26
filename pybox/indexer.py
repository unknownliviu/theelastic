import elasticsearch

import datetime
from strip import strip_html


def rightnow():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M:%S")


class Indexer:
    def __init__(self, index, input_file, reset=True):
        self.es = elasticsearch.Elasticsearch()
        self.index = index
        self.input_file = input_file
        if reset:
            self.reset_index(index)
        else:
            self.__create_index(index)
        self.html = strip_html(self.read())

    def reset_index(self, index):
        self.__destroy_index(index)
        self.__create_index(index)

    def __create_index(self, index):
        self.es.indices.create(index=index, ignore=400)

    def __destroy_index(self, index):
        self.es.indices.delete(index=index, ignore=[404])

    def read(self):
        with open(self.input_file, "r") as f:
            return f.read()

    def index_data(self):
        for idx, line in enumerate(self.html.split("\n")):
            self.es.index(
                index=self.index, id=idx, body={"indexed_at": rightnow(), "content": line, "file_name": self.input_file}
            )


if __name__ == "__main__":
    i = Indexer("html", "/app/data/bookns.html", True)
    i.index_data()
