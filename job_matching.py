from sentence_transformers import util

def match_jobs(portfolio_description, job_descriptions, model, top_k=20):
    """
    Match jobs to the portfolio description using cosine similarity.
    :param portfolio_description: The user's portfolio description.
    :param job_descriptions: List of job descriptions.
    :param model: The SBERT model for encoding.
    :param top_k: Number of top matches to retrieve.
    :return: List of matched jobs with similarity scores.
    """
    # Encode job descriptions and portfolio description
    job_embeddings = model.encode(job_descriptions, convert_to_tensor=True)
    portfolio_embedding = model.encode(portfolio_description, convert_to_tensor=True)

    # Compute cosine similarity scores
    similarity_scores = util.pytorch_cos_sim(portfolio_embedding, job_embeddings)

    # Sort job descriptions by similarity score
    top_results = similarity_scores[0].topk(top_k)

    return top_results
