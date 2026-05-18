from sentence_transformers import SentenceTransformer #AI model loader
from sklearn.metrics.pairwise import cosine_similarity #math function

# we usinhg th pre-trained Transformer-based NLP model below
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("dataset.txt", "r") as f: 
    #Removes extra spaces
    data = [line.strip() for line in f.readlines()]

#Converts each sentence into a vector (numbers) which rep 'meaning' not words
embeddings = model.encode(data)

#our rule-based decision system
def classify_risk(score):
    if score >= 0.45:
        return "HIGH"
    elif score >= 0.30:
        return "MEDIUM"
    else:
        return "LOW"

#takes user input -> compares it to dataset -> returns results
def search(query):
    query_vec = model.encode([query])
    scores = cosine_similarity(query_vec, embeddings)[0] #identical meaning is 1 and completely unrelated is 0

    results = []

    for i, score in enumerate(scores):
        if score > 0.25: #filter for meaningful results
            results.append({
                "text": data[i],
                "score": float(score),
                "risk": classify_risk(score)
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)