from sentence_transformers import SentenceTransformer #AI model loader
from sklearn.metrics.pairwise import cosine_similarity #math function
import re # regular expression

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
                "risk": classify_risk(score),
                "explanation": explain_match(query, data[i])
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)

def explain_match(query, sent):
    words = re.findall(r"\w+", sent)

    # get the original sentence score
    original = model.encode([sent])
    query_embed = model.encode([query])

    og_score = cosine_similarity(
        query_embed,
        original
    )[0][0]

    contributions = []

    for idx, word in enumerate(words):
        # start testing if this specific word was important
        removed = words[:idx] + words[idx+1:]
        new_sentence = " ".join(removed)

        # get new score
        new_embedding = model.encode([new_sentence])

        new_score = cosine_similarity(
            query_embed,
            new_embedding
        )[0][0]

        # check the score drop + remove negatives
        word_importance = max(0, og_score - new_score)

        contributions.append({
            "word": word,
            "importance": float(word_importance)
        })

    # normalise to percentages
    total = sum(c["importance"] for c in contributions)

    if total > 0:
        for c in contributions:
            c["importance"] /= total

    return contributions