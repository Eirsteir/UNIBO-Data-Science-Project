from src.models import Annotation


class Processor:
    def __init__(self):
        self.db_path_or_url = ""

    def get_db_path_or_url(self):
        return self.db_path_or_url

    def set_db_path_or_url(self, db_path_or_url):
        self.db_path_or_url = db_path_or_url


class QueryProcessor(Processor):

    def get_entity_by_id(self, id):
        raise NotImplementedError


class GenericQueryProcessor:
    def __init__(self):
        self.query_processors = []

    def clean_query_processors(self):
        self.query_processors = []

    def add_query_processor(self, query_processor):
        self.query_processors.append(query_processor)

    def get_all_annotations(self):
        annotations = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAllAnnotations"):
                annotations += query_processor.getAllAnnotations()
        return annotations

    def get_all_canvas(self):
        canvases = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "get_all_canvases"):
                canvases += query_processor.get_all_canvases()
        return canvases

    def get_all_collections(self):
        collections = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "get_all_collections"):
                collections += query_processor.get_all_collections()
        return collections

    def get_all_images(self):
        images = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "getAllImages"):
                images += query_processor.getAllImages()
        return images

    def get_all_manifests(self):
        collections = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "get_all_manifests"):
                collections += query_processor.get_all_manifests()
        return collections

    def get_all_annotations_to_canvas(self, canvas_id):
        annotations_to_canvas = []
        annotations = self.get_all_annotations()
        for annotation in annotations:
            for query_processor in self.query_processors:
                canvas = query_processor.get_entity_by_id(annotation.target)
            annotations_to_canvas += Annotation(annotation.id, annotation.body, canvas)

        return annotations

    def get_annotations_to_collection(self, collection_id):
        pass

    def get_annotations_to_manifest(self, manifest_id):
        pass

    def get_annotations_with_body(self, body_id):
        pass

    def get_annotations_with_target(self, target_id):
        pass

    def get_annotations_with_body_and_target(self, body_id, target_id):
        pass

    def get_canvases_in_collection(self, collection_id):
        canvases = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "get_canvases_in_collection"):
                canvases += query_processor.get_canvases_in_collection(collection_id)
        return canvases

    def get_canvases_in_manifest(self, manifest_id):
        canvases = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "get_canvases_in_manifest"):
                canvases += query_processor.get_canvases_in_manifest(manifest_id)
        return canvases

    def get_entity_by_id(self, id):
        for query_processor in self.query_processors:
            if entity := query_processor.get_entity_by_id(id):
                return entity
        return None

    def get_entities_with_creator(self, creator_name):
        pass

    def get_entities_with_label(self, label):
        entities = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "get_entities_with_label"):
                entities += query_processor.get_entities_with_label(label)
        return entities

    def get_entities_with_title(self, title):
        pass

    def get_images_annotating_canvas(self, canvas_id):
        pass

    def get_manifests_in_collection(self, collection_id):
        manifests = []
        for query_processor in self.query_processors:
            if hasattr(query_processor, "get_manifests_in_collection"):
                manifests += query_processor.get_manifests_in_collection(collection_id)
        return manifests
