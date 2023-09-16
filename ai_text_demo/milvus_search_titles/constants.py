from ai_text_demo.utils import relative_path_from_file

DATA_PATH = relative_path_from_file(__file__, 'data/New_Medium_Data.csv')
MILVUS_HOST = '127.0.0.1'
MILVUS_PORT = '19530'
COLLECTION_NAME = 'search_article_in_medium'
TITLE_VECTOR_LENGTH = 768
ENCODER_NAME = 'facebook/dpr-ctx_encoder-single-nq-base'
