

def hit_rate(pipeline,test_set:list[dict]) ->float:
    hit=0
    misses =[]
    for test_case in test_set:
        retrieved_data = pipeline.retriever.retrieve(test_case["question"])
        pages = [chunk["metadata"].get("page_number") for chunk in retrieved_data]
        
        if test_case["expected_page"] in pages:
            hit+=1  
        else:
            misses.append(test_case)
        
    return hit/len(test_set),misses
    
def mean_reciprocal_rank(pipeline ,test_set: list[dict]) ->float:
    total_rr=0.0
    for test_case in test_set:
        retrieved_docs = pipeline.retriever.retrieve(test_case["question"])
        expected_page = test_case["expected_page"]
        rr = 0.0
        for rank, doc in enumerate(retrieved_docs, start=1):
            if doc["metadata"].get("page_number") == expected_page:
                rr = 1.0 / rank
                break
        total_rr += rr
    return total_rr/len(test_set)
