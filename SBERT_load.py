from sentence_transformers import SentenceTransformer

def load_sbert_model(model_name='Nashhz/SBERT_KFOLD_User_Portfolio_to_Job_Descriptions'):
    """
    Load the SBERT model.
    :param model_name: Name of the model to load.
    :return: Loaded SBERT model.
    """
    try:
        model = SentenceTransformer(model_name)
        print("SBERT model loaded successfully.")
        return model
    except Exception as e:
        raise Exception(f"Error loading SBERT model: {e}")
