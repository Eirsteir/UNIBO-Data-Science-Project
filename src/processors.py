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
    def __init__(self, query_processors):
        self.query_processors = query_processors

    def clean_query_processors(self):
        self.query_processors = []

    def add_query_processor(self, query_processor):
        self.query_processors.append(query_processor)

    def get_all_annotations(self):
        pass

    def get_all_canvas(self):
        pass

    def get_all_collections(self):
        pass

    def get_all_images(self):
        pass

    def get_all_manifests(self):
        pass

    def get_all_annotations_to_canvas(self, canvas_id):
        pass

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
        pass

    def get_canvases_in_manifest(self, manifest_id):
        pass

    def get_entity_by_id(self, id):
        pass

    def get_entities_with_creator(self, creator_name):
        pass

    def get_entities_with_label(self, label):
        pass

    def get_entities_with_title(self, title):
        pass

    def get_images_annotating_canvas(self, canvas_id):
        pass

    def get_manifests_in_collection(self, collection_id):
        pass