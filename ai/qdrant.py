from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams\
    , Distance, Filter, FieldCondition, MatchValue, Range, PointStruct
from ai.embedding import embedd, build_text
from tools.stock_tools import get_all_stock
client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "stocks"


def create_collection(collection_name):
    try:

        collections = client.get_collections().collections
        names = [c.name for c in collections]  # append all returned collection to the list

        if collection_name not in names:
            client.create_collection(collection_name=collection_name, #recreate
                                     vectors_config=VectorParams(size=384, distance=Distance.COSINE))

            print(f"collection {collection_name} created")

        else:
            print(f"collection {collection_name} is already exist")
    except Exception as e:
        print(f"qdrant not running: {e}")
        exit(0)

def is_collection_empty(collection_name):

    count = client.count(collection_name=collection_name, exact=True)

    if count.count == 0:
        print(f"collection counter = {count.count}")
        return True
    else:
        print(f"collection counter = {count.count}")
        return False


def reload_data_to_qdrant():
    try:
        print("reloading data to qdrant")
        for item in get_all_stock():
            vector = embedd(build_text(item))
            client.upsert(collection_name=COLLECTION_NAME, points=[PointStruct(
                id=int(item["Code"]),  # id = str(uuid.uuid4())
                vector=vector,
                payload=item
            )])
    except:
        print("error while trying to reload data from json file to qdrant")

    print("items has been reloaded successfully")
    is_collection_empty(collection_name=COLLECTION_NAME)


def add_data_to_qdrant(item):
    vector = embedd(build_text(item))
    try:
        client.upsert(collection_name="stocks", points=[PointStruct(
            id=int(item["Code"]),  # id = str(uuid.uuid4())
            vector=vector,
            payload=item
        )])
    except:
        return 0


def build_qdrant_filter(filters):
    conditions = []

    for key, value in filters.items():
        if isinstance(value, dict):
            conditions.append(FieldCondition(key=key, range=Range(
                gte=value.get("gte"),
                lte=value.get("lte"),
                gt=value.get("gt"),
                lt=value.get("lt")
            )))
        else:
            conditions.append(FieldCondition(key=key,match=MatchValue(value=value)))
    return Filter(must=conditions)



    # docker run -p 6333:6333 qdrant/qdrant