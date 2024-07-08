import pandas as pd
'''
# Leggi il file excel originale
df = pd.read_excel("database-prova.xlsx")

# Reset dell'indice per aggiungere una colonna di ID univoci
df.reset_index(inplace=True)

# Rinomina la colonna dell'ID
df = df.rename(columns={'index': 'ID'})

# Rimuovi le righe in cui il valore della colonna "numero" è null
df = df.dropna(subset=["numero"])

# Converti la colonna "numero" in formato intero
df["numero"] = df["numero"].astype(int)

# Elimina la colonna che desideri rimuovere
df = df.drop(columns=['pagina_documento'])

df['data_conversazione'] = pd.to_datetime(df['data_conversazione'].astype(str)).dt.date

# Salva il nuovo dataset in un nuovo file csv
df.to_csv("convers_dataset.csv", index=False)
'''

# Leggi il file csv creato sopra
df = pd.read_csv("convers_dataset.csv")

# Inizializza il numero della conversazione corrente
current_conversation_number = None

# Inizializza il dizionario per mappare gli interlocutori agli alias
interlocutor_alias_mapping = {}

# Crea un nuovo DataFrame vuoto
new_df = pd.DataFrame()

# Loop attraverso ogni riga del DataFrame originale
for index, row in df.iterrows():
    print(f"Elaborazione della riga {index + 1}/{len(df)}...")
    # Salva il numero della conversazione corrente
    current_conversation_number = row["numero"]

    # Aggiorna il dizionario degli interlocutori e degli alias
    if pd.notna(row["alias_interlocutori"]):
        interlocutors = str(row["interlocutori"]).split(", ")
        aliases = str(row["alias_interlocutori"]).split(", ")
        interlocutor_alias_mapping = dict(zip(interlocutors, aliases))
    else:
        interlocutor_alias_mapping = {}

    # Assicurati che il valore nella cella "conversazione" sia di tipo stringa
    if isinstance(row["conversazione"], str):
        # Dividi la cella della conversazione in righe separate
        sentences = row["conversazione"].split("\n")  # Assumendo che le frasi siano separate da un ritorno a capo

        # Inizializza l'interlocutore corrente
        current_interlocutor = None
        complete_name_interlocutor = None

        # Loop attraverso ogni frase nella conversazione
        for sentence in sentences:
            # Verifica se la frase contiene il separatore " - "
            if " - " in sentence:
                # Estrai nome interlocutore e frase
                interlocutor, sentence = sentence.split(" - ", 1)

                # Verifica se l'interlocutore è presente nel dizionario e aggiorna l'interlocutore
                if interlocutor in interlocutor_alias_mapping.values():
                    for interl, alias in interlocutor_alias_mapping.items():
                        if alias == interlocutor:
                            complete_name_interlocutor = interl
                            break

                # Verifica se il nome dell'interlocutore è diverso da quello precedente
                if interlocutor != current_interlocutor:
                    # Aggiorna l'interlocutore corrente
                    current_interlocutor = interlocutor

            # Aggiungi la riga al nuovo DataFrame con il numero della conversazione corrente
            new_df = new_df.append({
                "ID": row["ID"],
                "tipologia": row["tipologia"],
                "numero": row["numero"],
                "luogo": row["luogo"],
                "data_conversazione": row["data_conversazione"],
                "orario_conversazione": row["orario_conversazione"],
                "lista_interlocutori": row["interlocutori"],
                "interlocutore": complete_name_interlocutor,
                "frase": sentence.strip()
            }, ignore_index=True)

# Sostituisci i valori nulli con un valore che indica che il dato non è stato fornito
valore_non_fornito = "N/A"
new_df['luogo'] = new_df['luogo'].fillna(valore_non_fornito)
new_df['orario_conversazione'] = new_df['orario_conversazione'].fillna(valore_non_fornito)

# Rimuovi le righe in cui la cella "Interlocutore" è vuota
new_df = new_df.dropna(subset=["interlocutore"])

# Rimuovi le righe in cui la cella "Frase" è vuota
new_df = new_df[new_df['frase'] != '']
new_df = new_df[new_df['frase'] != ' ']
new_df = new_df[new_df['frase'] != '\t']

# Converti le colonne "ID" e "numero" in interi
new_df["ID"] = new_df["ID"].astype(int)
new_df["numero"] = new_df["numero"].astype(int)

# Salva il nuovo dataset in un nuovo file csv
new_df.to_csv("frase_dataset.csv", index=False)

