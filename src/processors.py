import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore


class Processor:
    def __init__(self):
        self.db_path_or_url = ""

    def get_db_path_or_url(self):
        return self.db_path_or_url

    def set_db_path_or_url(self, db_path_or_url):
        self.db_path_or_url = db_path_or_url


class CollectionProcessor(Processor):
    # Define the namespaces used in the RDF schema
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    iiif = Namespace("http://iiif.io/api/presentation/3#")
    ex = Namespace("https://dl.ficlit.unibo.it/")

    def upload_data(self, filename):
        graph = self.__load_iiif_data_from_file(filename)
        self.__save_graph(graph)
        print("Finished uploading data!")

    def __load_iiif_data_from_file(self, filename):
        print("Loading rdf data from ", filename, "...")
        with open(filename) as f:
            collection_data = json.load(f)

        g = Graph()

        collection_id = collection_data["id"]
        collection_uri = URIRef(collection_id)
        g.add((collection_uri, RDF.type, self.iiif.Collection))
        g.add((collection_uri, self.iiif.label, Literal(collection_data["label"]["none"][0])))

        for manifest_data in collection_data["items"]:
            manifest_uri = URIRef(manifest_data["id"])
            g.add((manifest_uri, RDF.type, self.iiif.Manifest))
            g.add((manifest_uri, self.iiif.label, Literal(manifest_data["label"]["none"][0])))
            g.add((collection_uri, self.iiif.item, manifest_uri))

            for canvas_data in manifest_data["items"]:
                canvas_uri = URIRef(canvas_data["id"])
                g.add((canvas_uri, RDF.type, self.iiif.Canvas))
                g.add((canvas_uri, self.iiif.label, Literal(canvas_data["label"]["none"][0])))
                g.add((manifest_uri, self.iiif.item, canvas_uri))

        return g

    def __save_graph(self, graph):
        print("Saving graph to store...")
        store = SPARQLUpdateStore()

        store.open((self.db_path_or_url, self.db_path_or_url))

        for triple in graph.triples((None, None, None)):
            store.add(triple)

        store.close()


