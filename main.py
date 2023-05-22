from src.graph_processors import CollectionProcessor, TriplestoreQueryProcessor
from src.processors import GenericQueryProcessor

if __name__ == '__main__':
    grp_endpoint = 'http://127.0.0.1:8889/bigdata/sparql'
    col_dp = CollectionProcessor()

    # col_dp.set_db_path_or_url(grp_endpoint)
    # col_dp.upload_data("data/collection-1.json")
    # col_dp.upload_data("data/collection-2.json")

    grp_qp = TriplestoreQueryProcessor()
    # grp_qp.set_db_path_or_url(grp_endpoint)
    # res = grp_qp.get_entity_by_id("https://dl.ficlit.unibo.it/iiif/28429/collection")
    # print(res)

    generic_query_processor = GenericQueryProcessor()
    generic_query_processor.add_query_processor(grp_qp)
    generic_query_processor.get_all_annotations()
