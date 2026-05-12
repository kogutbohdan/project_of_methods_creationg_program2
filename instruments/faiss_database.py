import faiss
import numpy as np

indexId=faiss.IndexIDMap(faiss.IndexHNSWFlat(300, 32))


def do_search(vector,data):
    global indexId
    #print(vector)

    vectors=[]
    ids=[]

    for obj in data:
        ids.append(obj["id"])
        vectors.append(obj["vector"])
    if vectors and ids:
        vectors=np.array(vectors,dtype="float32")
        ids=np.array(ids,dtype="int64")
        indexId.add_with_ids(vectors,ids)
        score,result_ids=indexId.search(vector,10)
        indexId=faiss.IndexIDMap(faiss.IndexHNSWFlat(300, 32))
        return list(filter(lambda elem:elem!=-1,result_ids[0].tolist()))
    return []
