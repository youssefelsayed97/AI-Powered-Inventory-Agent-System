from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, results):
    top_r = 5
    pairs = []

    for r in results:
        pairs.append((query, r["cross_encoder_text"]))

    scores = model.predict(pairs)

    reranked = []

    # threshold = 1.0
    for r, score in zip(results, scores):
        # if score < threshold:
        #     continue
        reranked.append({
            "score": float(score),
            "result": r["payload"]

        })

    # reranked = sorted(reranked, key=lambda x: x["score"], reverse=True)

    return reranked[:top_r]
