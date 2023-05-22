from src.graph_processors import CollectionProcessor, TriplestoreQueryProcessor

if __name__ == '__main__':
    grp_endpoint = 'http://127.0.0.1:8889/bigdata/sparql'
    col_dp = CollectionProcessor()

    col_dp.set_db_path_or_url(grp_endpoint)
    col_dp.upload_data("data/collection-1.json")
    col_dp.upload_data("data/collection-2.json")

    grp_qp = TriplestoreQueryProcessor()
    grp_qp.set_db_path_or_url(grp_endpoint)
    res = grp_qp.get_entities_with_label("BO0451_CAM6537_0235_dorso.jpg")
    print(res)

