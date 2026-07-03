import json
import os

from ai.embedding import image_to_text, embedd
from ai.reranker import rerank
from dotenv import load_dotenv

load_dotenv()

STOCK_FILE = os.getenv("STOCK_FILE")


def get_all_stock():
    all_data = load_stock()
    return all_data["Stock"]


def load_stock():
    try:
        with open(STOCK_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "Stock": []
        }


def save_stock(data):
    with open(STOCK_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_stock(item):
    from ai.qdrant import add_data_to_qdrant
    all_data = load_stock()

    for data in all_data["Stock"]:

        if item["Code"] == data.get("Code"):
            return {
                        "success": False,
                        "message": "Item already exists"
                }

    item["ImageDescription"] = image_to_text(f"static/UPLOADS/{item.get('Image','')}")

    add_data_to_qdrant(item=item)

    all_data["Stock"].append(item)

    save_stock(all_data)

    return {
                "success": True,
                "message": "Item added successfully"
        }


def search_stock(semantic_query, filters):
    from ai.qdrant import client, build_qdrant_filter
    stock = []
    query_filter = build_qdrant_filter(filters)

    if semantic_query:
        query_vector = embedd(semantic_query)

        results = client.query_points(collection_name="stocks",
                                      query=query_vector,
                                      query_filter=query_filter,
                                      limit=10)

        products = [
            {
                "cross_encoder_text": f"{p.payload['Name']} {p.payload['ImageDescription']}",
                "payload": p.payload
            }
            for p in results.points
        ]

        final_result = rerank(semantic_query, products)

    else:
        all_results = []
        offset = None
        while True:

            results, offset = client.scroll(
                                            collection_name="stocks",
                                            scroll_filter=query_filter,
                                            limit=100,
                                            offset=offset
                                  )
            all_results.extend([p.payload for p in results])
            if offset is None:
                break
        final_result = all_results
    try:

        for r in final_result:
            item = r["result"] if "result" in r else r

            stock.append({
                "Name": item["Name"],
                "Code": item["Code"],
                "LowPrice": item["LowPrice"],
                "HighPrice": item["HighPrice"],
                "Source": item["Source"],
                "Image": item["Image"],
                "ImageDescription": item["ImageDescription"]
            })

        return {
                "tool": "search_stock",
                "success": True,
                "result": stock
        }
    except:
        return {
            "tool": "search_stock",
            "success": False,
            "result": None
        }


def delete_stock(code):

    all_data = load_stock()

    new_stock = []

    deleted_item = None

    for item in all_data["Stock"]:
        if int(item["Code"]) == int(code):
            deleted_item = item
        else:
            new_stock.append(item)

    if deleted_item is None:
        return {
            "tool": "delete_stock",
            "success": False,
            "message": "Item not found"
        }

    all_data["Stock"] = new_stock

    save_stock(all_data)

    return {
        "tool": "delete_stock",
        "success": True,
        "message": "Item has been deleted",
        "deleted_item": deleted_item
    }
