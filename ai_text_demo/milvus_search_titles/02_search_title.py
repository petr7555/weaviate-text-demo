import numpy as np
from towhee import ops, pipe, DataCollection

from constants import COLLECTION_NAME, MILVUS_HOST, MILVUS_PORT, ENCODER_NAME

search_pipe = (pipe.input('query')
               .map('query', 'vec', ops.text_embedding.dpr(model_name=ENCODER_NAME))
               .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
               .flat_map('vec', ('id', 'score'), ops.ann_search.milvus_client(host=MILVUS_HOST,
                                                                              port=MILVUS_PORT,
                                                                              collection_name=COLLECTION_NAME))
               .output('query', 'id', 'score')
               )

print('Search one text in Milvus')
res = search_pipe('funny python demo')
DataCollection(res).show()

print('Search multi text in Milvus')
res = search_pipe.batch(['funny python demo', 'AI in data analysis'])
for re in res:
    DataCollection(re).show()

print('Search text and return multi fields')
search_pipe1 = (pipe.input('query')
                .map('query', 'vec', ops.text_embedding.dpr(model_name=ENCODER_NAME))
                .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
                .flat_map('vec', ('id', 'score', 'title'), ops.ann_search.milvus_client(host=MILVUS_HOST,
                                                                                        port=MILVUS_PORT,
                                                                                        collection_name=COLLECTION_NAME,
                                                                                        output_fields=['title']))
                .output('query', 'id', 'score', 'title')
                )

res = search_pipe1('funny python demo')
DataCollection(res).show()

search_pipe2 = (pipe.input('query')
                .map('query', 'vec', ops.text_embedding.dpr(model_name=ENCODER_NAME))
                .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
                .flat_map('vec', ('id', 'score', 'title', 'link', 'reading_time', 'publication', 'claps', 'responses'),
                          ops.ann_search.milvus_client(host=MILVUS_HOST,
                                                       port=MILVUS_PORT,
                                                       collection_name=COLLECTION_NAME,
                                                       output_fields=['title', 'link', 'reading_time', 'publication',
                                                                      'claps', 'responses'],
                                                       limit=5))
                .output('query', 'id', 'score', 'title', 'link', 'reading_time', 'publication', 'claps', 'responses')
                )

res = search_pipe2('funny python demo')
DataCollection(res).show()

print('Search text with some expression')
search_pipe3 = (pipe.input('query')
                .map('query', 'vec', ops.text_embedding.dpr(model_name=ENCODER_NAME))
                .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
                .flat_map('vec', ('id', 'score', 'title', 'link', 'reading_time', 'publication', 'claps', 'responses'),
                          ops.ann_search.milvus_client(host=MILVUS_HOST,
                                                       port=MILVUS_PORT,
                                                       collection_name=COLLECTION_NAME,
                                                       expr='title like "Python%"',
                                                       output_fields=['title', 'link', 'reading_time', 'publication',
                                                                      'claps', 'responses'],
                                                       limit=5))
                .output('query', 'id', 'score', 'title', 'link', 'reading_time', 'publication', 'claps', 'responses')
                )

res = search_pipe3('funny python demo')
DataCollection(res).show()
