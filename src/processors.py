class Processor:
    def __init__(self):
        self.db_path_or_url = ""

    def get_db_path_or_url(self):
        return self.db_path_or_url

    def set_db_path_or_url(self, db_path_or_url):
        self.db_path_or_url = db_path_or_url

