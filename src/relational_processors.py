import pandas as pd
from sqlite3 import connect

from processors import Processor


class AnnotationProcessor(Processor):

    def uploadData(self, path):

        annotations = pd.read_csv(path,
                                  keep_default_na=False,
                                  dtype={
                                      "id": "string",
                                      "motivation": "string",
                                      "target": "string",
                                      "body": "string"
                                  })

        db = self.get_db_path_or_url()

        with connect(db) as con:
            annotations.to_sql(
                "Annontations", con, if_exists="replace", index=False)

        return True


class MetadataProcessor(Processor):

    def uploadData(self, path):

        metadata = pd.read_csv(path,
                               keep_default_na=False,
                               dtype={
                                   "id": "string",
                                   "title": "string",
                                   "creator": "string",
                               })

        db = self.get_db_path_or_url()

        with connect(db) as con:
            metadata.to_sql(
                "Metadata", con, if_exists="replace", index=False)
        return True


class RelationalQueryProcessor(QueryProcessor):

    def getAllAnnotations(self):

        db = 0  # TODO

        with connect(db) as con:
            query = "SELECT * FROM Annontations"
            df_annontations_sql = pd.read_sql(query, con)

        return df_annontations_sql

    def getAllImages(self):

        db = 0  # TODO
        with connect(db) as con:
            query = "SELECT body FROM Annontations"
            df_images_sql = pd.read_sql(query, con)

        return df_images_sql

    def getAnnotationsWithBody(self, body):

        db = 0  # TODO
        with connect(db) as con:
            query = "SELECT * FROM Annontations WHERE body={body}"
            df_annontations_with_image_sql = pd.read_sql(query, con)

        return df_annontations_with_image_sql

    def getAnnotationsWithBodyAndTarget(self, body, target):

        db = 0  # TODO
        with connect(db) as con:
            query = "SELECT * FROM Annontations WHERE body={body} AND target={target}"
            df_annontations_with_image_and_target_sql = pd.read_sql(query, con)

        return df_annontations_with_image_and_target_sql

    def getEntitiesWithCreator(self, creator):

        db = 0  # TODO
        with connect(db) as con:
            query = "SELECT * FROM Metadata WHERE creator={creator}"
            df_metadata_with_creator_sql = pd.read_sql(query, con)

        return df_metadata_with_creator_sql

    def getEntitiesWithLabel(self, label):

        db = 0  # TODO
        with connect(db) as con:
            query = "SELECT * FROM Metadata WHERE label={label}"
            df_metadata_with_label_sql = pd.read_sql(query, con)

        return df_metadata_with_label_sql

    def getEntitiesWithTitle(self, title):

        db = 0  # TODO
        with connect(db) as con:
            query = "SELECT * FROM Metadata WHERE title={title}"
            df_metadata_with_title_sql = pd.read_sql(query, con)

        return df_metadata_with_title_sql
