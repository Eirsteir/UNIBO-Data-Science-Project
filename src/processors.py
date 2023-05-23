from src.models import Annotation, Image, Canvas, Collection, Manifest, IdentifiableEntity, EntityWithMetadata


class Processor:
    def __init__(self):
        self.db_path_or_url = ""

    def getDbPathOrUrl(self):
        return self.db_path_or_url

    def setDbPathOrUrl(self, db_path_or_url):
        self.db_path_or_url = db_path_or_url
        return True

class QueryProcessor(Processor):

    def getEntityById(self, id):
        pass


class GenericQueryProcessor:
    def __init__(self):
        self.query_processors = []

    def cleanQueryProcessors(self):
        self.query_processors = []
        return True

    def addQueryProcessor(self, query_processor):
        self.query_processors.append(query_processor)
        return True

    def getAllAnnotations(self):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAllAnnotations"):
                df = query_processor.getAllAnnotations()
                result += [(Annotation(row.id, row.motivation, row.body, row.target)) for index, row in df.iterrows()]

        return result

    def getAllCanvas(self):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAllCanvases"):
                df = query_processor.getAllCanvases()
                result += [(Canvas(row.canvas)) for index, row in df.iterrows()]

        return result

    def getAllCollections(self):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAllCollections"):
                df = query_processor.getAllCollections()
                result += [(Collection(row.collection, [])) for index, row in df.iterrows()]

        return result

    def getAllImages(self):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAllImages"):
                df = query_processor.getAllImages()
                result += [(Image(row)) for index, row in df.iterrows()]  # TODO: dobbeltsjekk

        return result

    def getAllManifests(self):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAllManifests"):
                df = query_processor.getAllManifests()
                result += [(Manifest(row.manifest, [])) for index, row in df.iterrows()]

        return result

    def getAnnotationsToCanvas(self, canvas_id):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAnnotationsWithTarget"):
                df = query_processor.getAnnotationsWithTarget(canvas_id)
                canvas = self.getEntityById(canvas_id)
                result += [(Annotation(row.id, row.motivation, row.body, canvas)) for index, row in df.iterrows()]

        return result

    def getAnnotationsToCollection(self, collection_id):  # vent
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getCanvasesInCollection"):
                df = query_processor.getCanvasesInCollection(collection_id)
                print("DF:", df)
                if df is not None and not df.empty:
                    for _id in df.canvas.values:
                        result += self.getAnnotationsWithTarget(_id)

        return result

    def getAnnotationsToManifest(self, manifest_id):  # vent
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getCanvasesInCollection"):
                df = query_processor.getCanvasesInManifest(manifest_id)
                if df is not None and not df.empty:
                    for _id in df.canvas.values:
                        result += self.getAnnotationsWithTarget(_id)

        return result

    def getAnnotationsWithBody(self, body_id):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAnnotationsWithBody"):
                df = query_processor.getAnnotationsWithBody(body_id)
                result += [(Annotation(row.id, row.motivation, row.body, row.target)) for index, row in df.iterrows()]

        return result

    def getAnnotationsWithTarget(self, target_id):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAnnotationsWithTarget"):
                df = query_processor.getAnnotationsWithTarget(target_id)
                result += [(Annotation(row.id, row.motivation, row.body, row.target)) for index, row in df.iterrows()]

        return result

    def getAnnotationsWithBodyAndTarget(self, body_id, target_id):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAnnotationsWithBodyAndTarget"):
                df = query_processor.getAnnotationsWithBodyAndTarget(body_id, target_id)
                result += [(Annotation(row.id, row.motivation, row.body, row.target)) for index, row in df.iterrows()]

        return result

    def getCanvasesInCollection(self, collection_id):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getCanvasesInCollection"):
                df = query_processor.getCanvasesInCollection(collection_id)
                result += [(Canvas(row.canvas)) for index, row in df.iterrows()]

        return result

    def getCanvasesInManifest(self, manifest_id):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getCanvasesInManifest"):
                df = query_processor.getCanvasesInManifest(manifest_id)
                result += [(Canvas(row.canvas)) for index, row in df.iterrows()]

        return result

    def getEntityById(self, id):
        for query_processor in self.query_processors:
            entity_df = query_processor.getEntityById(id)
            if entity_df is not None and not entity_df.empty:
                return IdentifiableEntity(entity_df.iloc[0])
        return IdentifiableEntity(id)

    def getEntitiesWithCreator(self, creator_name):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getEntitiesWithCreator"):
                df = query_processor.getEntitiesWithCreator(creator_name)
                result += [(EntityWithMetadata(row.id, "", row.title, row.creator)) for index, row in df.iterrows()]

        return result

    def getEntitiesWithLabel(self, label):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getEntitiesWithLabel"):
                df = query_processor.getEntitiesWithLabel(label)
                result += [(EntityWithMetadata(row.entity, "", "", "")) for index, row in df.iterrows()]

        return result

    def getEntitiesWithTitle(self, title):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getEntitiesWithTitle"):
                df = query_processor.getEntitiesWithTitle(title)
                result += [(EntityWithMetadata(row.id, "", row.title, row.creator)) for index, row in df.iterrows()]

        return result

    def getImagesAnnotatingCanvas(self, canvas_id):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAnnotationsWithTarget"):
                annotations = self.getAnnotationsWithTarget(canvas_id)
                for annotation in annotations:
                    result += [Image(annotation.body)]

        return result

    def getManifestsInCollection(self, collection_id):
        result = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getManifestsInCollection"):
                df = query_processor.getManifestsInCollection(collection_id)
                result += [(Manifest(row, [])) for index, row in df.iterrows()]

        return result
