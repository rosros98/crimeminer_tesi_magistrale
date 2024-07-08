import matplotlib.pyplot as plt
from app.repositories.Entity.InterlocutoreRepository import IndividualEmotionInfoRepository  

# Funzione per creare un grafico a barre delle emozioni prevalenti
def create_bar_chart(start_date, end_date):
    # Istanzia il repository per le informazioni sull'emozione individuale
    repo = IndividualEmotionInfoRepository(csv_file_path="data/frase_sentiment_emotion_modificato.csv")
    
    # Calcola le emozioni prevalenti nell'intervallo di tempo specificato
    prevalent_emotions = repo.calculate_prevalent_emotion(start_date, end_date)
    
    # Estrai i nomi degli individui e le emozioni prevalenti
    individuals = list(prevalent_emotions.keys())
    emotions = list(prevalent_emotions.values())
    
    # Crea il grafico a barre
    plt.figure(figsize=(10, 6))
    plt.barh(individuals, emotions, color='skyblue')
    plt.xlabel('Prevalent Emotion')
    plt.ylabel('Individual')
    plt.title('Prevalent Emotions for Individuals')
    plt.grid(True)
    plt.tight_layout()
    
    # Salva il grafico come immagine
    plt.savefig('prevalent_emotions_bar_chart.png')
    plt.close()

# Esempio di intervallo di tempo
start_date = '2004-01-06'
end_date = '2004-01-31'

# Chiamata alla funzione per creare il grafico a barre delle emozioni prevalenti
create_bar_chart(start_date, end_date)

# utils.py

