from src.processors import CollectionProcessor

if __name__ == '__main__':
    grp_endpoint = 'http://127.0.0.1:8889/bigdata/sparql'
    col_dp = CollectionProcessor()
    col_dp.set_db_path_or_url(grp_endpoint)
    col_dp.upload_data("data/collection-1.json")
    col_dp.upload_data("data/collection-2.json")
