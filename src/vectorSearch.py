from qdrant_client import QdrantClient
import time
import threading
import json

cfg = json.load(open('./src/config.json'))

host = cfg['host']
port = cfg['port']

qdrant_client = QdrantClient(host=host, port=port)

collections = cfg['collections']


def run(c, limit, vector):
    global payload
    search_result = qdrant_client.search(
        collection_name=c,
        query_vector=vector,
        query_filter=None,
        limit=limit
    )
    payload = payload + [[hit.id, hit.score, c] for hit in search_result]


def search(vector, limit, pool_id):
    global payload

    st = time.time()

    payload = []
    if len(pool_id) == 0:
        c = collections
    else:
        c = [collections[int(x)] for x in pool_id]
    th = []
    for i in c:
        th.append(threading.Thread(target=run, args=[i, limit, vector]))
        th[-1].start()
    for i in th:
        i.join()

    payload.sort(key=lambda x: x[1], reverse=True)
    print(time.time() - st)

    return payload[:limit]
