import json

from sparql_dataframe import get
from rdflib import Graph, Namespace, URIRef, Literal, RDF
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

from src.processors import Processor

# Define the namespaces used in the RDF schema
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
iiif = Namespace("http://iiif.io/api/presentation/3#")
ex = Namespace("https://dl.ficlit.unibo.it/")


class CollectionProcessor(Processor):

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
        g.add((collection_uri, RDF.type, iiif.Collection))
        g.add((collection_uri, iiif.label, Literal(collection_data["label"]["none"][0])))

        for manifest_data in collection_data["items"]:
            manifest_uri = URIRef(manifest_data["id"])
            g.add((manifest_uri, RDF.type, iiif.Manifest))
            g.add((manifest_uri, iiif.label, Literal(manifest_data["label"]["none"][0])))
            g.add((collection_uri, iiif.item, manifest_uri))

            for canvas_data in manifest_data["items"]:
                canvas_uri = URIRef(canvas_data["id"])
                g.add((canvas_uri, RDF.type, iiif.Canvas))
                g.add((canvas_uri, iiif.label, Literal(canvas_data["label"]["none"][0])))
                g.add((manifest_uri, iiif.item, canvas_uri))

        return g

    def __save_graph(self, graph):
        print("Saving graph to store...")
        store = SPARQLUpdateStore()

        store.open((self.db_path_or_url, self.db_path_or_url))

        for triple in graph.triples((None, None, None)):
            store.add(triple)

        store.close()


class TriplestoreQueryProcessor(Processor):

    PREFIXES = f"""
        PREFIX rdf:  <{rdf}>
        PREFIX ex: <{ex}>
        PREFIX iiif: <{iiif}>
    """

    def get_all_canvases(self):
        query = f"""
        {self.PREFIXES}

        SELECT ?canvas
        WHERE {{
          ?canvas a iiif:Canvas
        }}
        """
        return get(self.db_path_or_url, query, True)

    def get_all_collections(self):
        query = f"""
         {self.PREFIXES}

         SELECT ?collection
         WHERE {{
           ?collection a iiif:Collection
         }}
         """
        return get(self.db_path_or_url, query, True)

    def get_all_manifests(self):
        query = f"""
         {self.PREFIXES}

         SELECT ?manifest
         WHERE {{
           ?manifest a iiif:Manifest
         }}
         """
        return get(self.db_path_or_url, query, True)

    def get_canvases_in_collection(self, collection_id):
        query = f"""
         {self.PREFIXES}
         
        SELECT ?canvas
        WHERE {{
          <{collection_id}> iiif:item ?manifest .
          ?manifest iiif:item ?canvas . 
          ?canvas a iiif:Canvas .
        }}
         """
        return get(self.db_path_or_url, query, True)

    def get_canvases_in_manifest(self, manifest_id):
        query = f"""
         {self.PREFIXES}

        SELECT ?canvas
        WHERE {{
            <{manifest_id}> iiif:item ?canvas .
            ?canvas a iiif:Canvas .
        }}
         """
        return get(self.db_path_or_url, query, True)

    def get_entities_with_label(self, label):
        pass

    def get_manifests_in_collection(self, collection_id):
        pass