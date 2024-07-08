import pandas as pd
from feel_it.feel_it_modificato import EmotionClassifier

# Funzione per ottenere l'emozione con relativa confidenza
def get_emotion(frase, emotion_classifier, index):
    print(f"Sto assegnando l'emozione - Riga: {index + 1}")
    emotions_with_confidences = emotion_classifier.predict_emotmod([frase])[0]
    return ", ".join([f"{emotion} ({confidence:.7f})" for emotion, confidence in emotions_with_confidences])

# Funzione per estrarre l'emozione con il valore più alto
def extract_highest_emotion(emozioni, index):
    print(f"Sto estraendo l'emozione più alta - Riga: {index + 1}")
    emotions = [emozione.split('(') for emozione in emozioni.split(',')]
    emotions_confidences = [(emozione.strip(), float(confidence[:-1])) for emozione, confidence in emotions]
    highest_emotion = max(emotions_confidences, key=lambda x: x[1])
    return highest_emotion[0]

# Carica il dataset
df = pd.read_csv("frase_sentiment_analysis.csv")
print("Ho letto il dataset...")

# Inizializza il classificatore di emozioni e sentimenti
emotion_classifier = EmotionClassifier()
print("Ho inizializzato...")

# Aggiungi la colonna "lista_emozioni" al DataFrame
df['lista_emozioni'] = df.apply(lambda row: get_emotion(row['frase'], emotion_classifier, row.name), axis=1)

# Estrai l'emozione con il valore più alto e aggiungila alla colonna "emozione"
df['emozione'] = df.apply(lambda row: extract_highest_emotion(row['lista_emozioni'], row.name), axis=1)

# Salva il nuovo dataset con le colonne aggiunte
df.to_csv('frase_sentiment_emotion.csv', index=False)
print("Elaborazione completata!")
