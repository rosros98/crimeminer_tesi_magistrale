import pandas as pd

# Definisci il percorso del file CSV
csv_file_path = "dataset_finale/finale_sentimento_emozione.csv"

# Leggi il file CSV utilizzando pandas
df = pd.read_csv(csv_file_path)

# Specifica il valore da utilizzare per la sostituzione dei valori nulli
valore_non_fornito = "dato non fornito"

# Sostituisci i valori nulli con la stringa indicata (eccetto 'data_conversazione')
for colonna in df.columns:
    if colonna != 'data_conversazione':
        df[colonna].fillna(valore_non_fornito, inplace=True)

# Gestisci i valori nulli nella colonna 'data_conversazione'
df['data_conversazione'].fillna('1900-01-01', inplace=True)  # Usa una data fittizia per i valori nulli
df['data_conversazione'] = pd.to_datetime(df['data_conversazione'].astype(str), errors='coerce').dt.date

# Trasforma la colonna ID in interi
df["ID"] = df["ID"].astype(int)

# Colonne da trasformare in minuscolo
colonne_da_trasformare = ["luogo", "interlocutore", "lista_interlocutori", "frase", "numero"]

# Trasforma il contenuto delle colonne specifiche in minuscolo
for colonna in colonne_da_trasformare:
    if colonna in df.columns:  # Verifica che la colonna esista nel DataFrame
        df[colonna] = df[colonna].str.lower()

# Salva il DataFrame modificato in un nuovo file CSV
df.to_csv("crimeminer_finale.csv", index=False)