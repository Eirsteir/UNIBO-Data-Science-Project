import json

from sparql_dataframe import get
from rdflib import Graph, Namespace, URIRef, Literal, RDF
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

from src.processors import Processor, QueryProcessor

# Define the namespaces used in the RDF schema
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
iiif = Namespace("http://iiif.io/api/presentation/3#")
ex = Namespace("https://dl.ficlit.unibo.it/")


class CollectionProcessor(Processor):

    def uploadData(self, filename):
        graph = self.__load_iiif_data_from_file(filename)
        self.__save_graph(graph)
        print("Finished uploading data!")
        return True

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


class TriplestoreQueryProcessor(QueryProcessor):

    PREFIXES = f"""
        PREFIX rdf:  <{rdf}>
        PREFIX ex: <{ex}>
        PREFIX iiif: <{iiif}>
    """

    def getEntityById(self, id):
        query = f"""
        {self.PREFIXES}

        SELECT * 
        WHERE {{ 
            <{id}> rdf:type ?o . 
        }}
        """
        return get(self.db_path_or_url, query, True)

    def getAllCanvases(self):
        query = f"""
        {self.PREFIXES}

        SELECT ?canvas
        WHERE {{
          ?canvas a iiif:Canvas
        }}
        """
        return get(self.db_path_or_url, query, True)

    def getAllCollections(self):
        query = f"""
         {self.PREFIXES}

         SELECT ?collection
         WHERE {{
           ?collection a iiif:Collection
         }}
         """
        return get(self.db_path_or_url, query, True)

    def getAllManifests(self):
        query = f"""
         {self.PREFIXES}

         SELECT ?manifest
         WHERE {{
           ?manifest a iiif:Manifest
         }}
         """
        return get(self.db_path_or_url, query, True)

    def getCanvasesInCollection(self, collection_id):
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

    def getCanvasesInManifest(self, manifest_id):
        query = f"""
         {self.PREFIXES}

        SELECT ?canvas
        WHERE {{
            <{manifest_id}> iiif:item ?canvas .
            ?canvas a iiif:Canvas .
        }}
         """
        return get(self.db_path_or_url, query, True)

    def getEntitiesWithLabel(self, label):
        query = f"""
         {self.PREFIXES}

        SELECT ?entity 
        WHERE {{
          ?entity iiif:label '{label}'
        }}
        """
        return get(self.db_path_or_url, query, True)

    def getManifestsInCollection(self, collection_id):
        query = f"""
        {self.PREFIXES}
        
        SELECT ?manifest
        WHERE {{
          <{collection_id}> iiif:item ?manifest .
          ?manifest a iiif:Manifest .
        }}
        """
        return get(self.db_path_or_url, query, True)