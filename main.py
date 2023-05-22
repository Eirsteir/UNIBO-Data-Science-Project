# from src.graph_processors import CollectionProcessor, TriplestoreQueryProcessor
from src.relational_processors import AnnotationProcessor, MetadataProcessor, RelationalQueryProcessor

if __name__ == '__main__':
    '''grp_endpoint = 'http://127.0.0.1:8889/bigdata/sparql'
    col_dp = CollectionProcessor()

    # col_dp.set_db_path_or_url(grp_endpoint)
    # col_dp.upload_data("data/collection-1.json")
    # col_dp.upload_data("data/collection-2.json")

    grp_qp = TriplestoreQueryProcessor()
    grp_qp.set_db_path_or_url(grp_endpoint)
    res = grp_qp.get_entity_by_id("https://dl.ficlit.unibo.it/iiif/28429/collection")
    print(res)'''

    rel_path = "relational.db"

    '''ann_dp = AnnotationProcessor()
    ann_dp.set_db_path_or_url(rel_path)
    ann_dp.uploadData("data/annotations.csv")

    met_dp = MetadataProcessor()
    met_dp.set_db_path_or_url(rel_path)
    met_dp.uploadData("data/metadata.csv")'''

    rel_qp = RelationalQueryProcessor()
    rel_qp.set_db_path_or_url(rel_path)
    res = rel_qp.getEntitiesWithTitle("Raimondi, Giuseppe")
    print(res)
