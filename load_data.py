import pandas as pd

# Definisci la funzione per leggere e preparare i dati
def read_and_prepare_data(csv_file_path):
    # Leggi il file CSV utilizzando pandas
    df = pd.read_csv(csv_file_path)

    # Verifica se ci sono valori nulli nel DataFrame
    print(df.isnull().sum())

    # Specifica il valore da utilizzare per la sostituzione
    valore_non_fornito = "dato non fornito"

    # Itera sul DataFrame e sostituisci manualmente i valori nulli
    for colonna in df.columns:
        df[colonna].fillna(valore_non_fornito, inplace=True)

    # Verifica se ci sono valori nulli nel DataFrame dopo la sostituzione
    print(df.isnull().sum())

    # Salva il DataFrame modificato in un nuovo file CSV
    df.to_csv("data/frase_sentiment_emotion_modificato.csv", index=False)

    # Restituisci il DataFrame preparato
    return df

# Definisci il percorso del file CSV originale
csv_file_path = "data/frase_sentiment_emotion.csv"

# Chiama la funzione per leggere e preparare i dati
df = read_and_prepare_data(csv_file_path)
