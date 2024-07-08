import pandas as pd
import torch
from torch import nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Carica il tokenizer e il modello
tokenizer = AutoTokenizer.from_pretrained("neuraly/bert-base-italian-cased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("neuraly/bert-base-italian-cased-sentiment")

# Carica il file csv
df = pd.read_csv("frase_dataset.csv")

# Funzione per applicare il modello BERT sentiment a ogni frase
def predict_sentiment(sentence):
    input_ids = tokenizer.encode(sentence, add_special_tokens=True, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(input_ids)[0]
    proba = nn.functional.softmax(logits, dim=1)
    return proba.squeeze(0)

# # Funzione per applicare il modello BERT sentiment a ogni conversazione considerando un limite di token
# def predict_sentiment(sentence):
#     # Limite lunghezza frase (512 valore massimo di parole che un modello BERT può considerare)
#     max_length = 280 #essendo le conversazioni divise in singole frasi da analizzare non è necessario considerare il limite massimo
#     sentence = sentence[:max_length]
#     input_ids = tokenizer.encode(sentence, add_special_tokens=True, return_tensors="pt", max_length=max_length, truncation=True)
#     with torch.no_grad():
#         logits = model(input_ids)[0]
#     proba = nn.functional.softmax(logits, dim=1)
#     return proba.squeeze(0)

# Funzione per estrarre il sentimento dominante
def get_dominant_sentiment(row):
    print(f"Stabilisco sentimento predominante - {row.name}/{len(df)}")
    if isinstance(row['frase'], str):  # Verifica se la cella è una stringa
        probabilities = predict_sentiment(row['frase'])
        negative, neutral, positive = probabilities.tolist()
        sentiment_label = max((negative, "NEGATIVE"), (neutral, "NEUTRAL"), (positive, "POSITIVE"))[1]
        return sentiment_label
    else:
        return ""

# Aggiunta di una nuova colonna al dataframe per indicare il sentimento dominante
df['sentimento'] = df.apply(get_dominant_sentiment, axis=1)

# Salvataggio del dataframe nel file CSV
df.to_csv("frase_sentiment_analysis.csv", index=False)
print("Elaborazione completata!")