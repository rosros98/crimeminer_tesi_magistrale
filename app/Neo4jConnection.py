from neo4j import GraphDatabase
from neomodel import config
import pandas as pd

class Neo4jDriver:
    _uri = "bolt://localhost:7687"
    _user = "neo4j"
    _password = "neo44%*j"
    _driver = None

    @classmethod
    def initialize(cls):
        config.DATABASE_URL = f'bolt://{cls._user}:{cls._password}@localhost:7687'
        if cls._driver is None:
            cls._driver = GraphDatabase.driver(cls._uri, auth=(cls._user, cls._password))
            session = Neo4jDriver.get_session()

            Creazione_grafico_ProfiloCriminale = "CALL gds.graph.project('ProfiloCriminale', 'Interlocutore', 'HaConversato'})"
            session.run(Creazione_grafico_ProfiloCriminale)
            
            Creazione_grafico_IndInt = "CALL gds.graph.project('IndividuoIntercettazioni', 'Individuo', 'HaChiamato' ,{relationshipProperties: 'mesiTotali'})"
            session.run(Creazione_grafico_IndInt)
            
            Creazione_grafico_IndReaCloBet = "CALL gds.graph.project('IndividuoReatiCloBet', ['Individuo','Reato'],{ImputatoDi: {orientation: 'UNDIRECTED'}, Condannato:{orientation: 'UNDIRECTED'} },{relationshipProperties: 'mesiTotali'})"
            session.run(Creazione_grafico_IndReaCloBet)
            Creazione_grafico_IndRea = "CALL gds.graph.project('IndividuoReati', ['Individuo','Reato'],['ImputatoDi','Condannato'],{relationshipProperties: 'mesiTotali'})"
            session.run(Creazione_grafico_IndRea)

            Creazione_grafico_IndIntAmbCloBet = "CALL gds.graph.project('IndividuoIntercettazioneAmbCloBet', ['Individuo','IntercettazioneAmb'],{Presente: {orientation:'UNDIRECTED'} },{relationshipProperties: 'mesiTotali'})"
            session.run(Creazione_grafico_IndIntAmbCloBet)
            Creazione_grafico_IndIntAmb = "CALL gds.graph.project('IndividuoIntercettazioneAmb', ['Individuo','IntercettazioneAmb'],'Presente',{relationshipProperties: 'mesiTotali'})"
            session.run(Creazione_grafico_IndIntAmb)
           
            Creazione_grafico_IndReatoIntAmbCloBet = "CALL gds.graph.project('IndividuoReatoIntercettazioneAmbCloBet', ['Individuo','IntercettazioneAmb','Reato'], {HaChiamato: {orientation:'UNDIRECTED'},ImputatoDi: { orientation:'UNDIRECTED'},Condannato: {orientation: 'UNDIRECTED'},Presente: {orientation: 'UNDIRECTED' } } ,{relationshipProperties: 'mesiTotali'})"
            session.run(Creazione_grafico_IndReatoIntAmbCloBet)
            Creazione_grafico_IndReatoIntAmb = "CALL gds.graph.project('IndividuoReatoIntercettazioneAmb', ['Individuo','IntercettazioneAmb','Reato'], ['HaChiamato','ImputatoDi','Condannato','Presente'],{relationshipProperties: 'mesiTotali'})"
            session.run(Creazione_grafico_IndReatoIntAmb)
            
    @classmethod
    def close(cls):
        if cls._driver is not None: 
            cls._driver.close()
            cls._driver = None

    @classmethod
    def get_session(cls):
        if cls._driver is None:
            cls.initialize()
        return cls._driver.session()

#################################################### QUERY EFFETTUATE PER CARICAMENTO DATI E CREAZIONE NUOVI GRAFICI PER NEO4J ##############################################################
"""Le query riportate devono essere eseguite nell'ordine indicato"""       
""" query1 per il caricamento del file csv """   
            # query1 = """
            #     LOAD CSV WITH HEADERS FROM 'file:///frase_sentiment_emotion_modificato.csv' AS row          
            #     MERGE (i:Interlocutore {nome: trim(row.interlocutore)}) 
            #     WITH i, row
            #     ORDER BY row.ID
            #     WITH i, collect(row) AS rows
            #     SET i.info_conversazioni = reduce(s = "", x in rows | 
            #         s + '{'+ '\nID: ' + x.ID + ',\nemozione: ' + x.emozione + ',\nsentimento: ' + x.sentimento + ',\ntipologia: ' + x.tipologia + ',\nnumero: ' + x.numero + ',\nluogo: ' + x.luogo + ',\nlista_interlocutori: ' + x.lista_interlocutori + ',\ndata_conversazione: ' + x.data_conversazione + ',\norario_conversazione: ' + x.orario_conversazione + ',\nfrase: ' + x.frase + '}'
            #     )
            #     RETURN count(i);
            # """         
            # session.run(query1)

""" query3 ha permesso l'aggiunta di proprietà con valoer non fornito al grafo Interlocutore """
            # query3 = """
            # MATCH (m:Interlocutore)
            # SET m.provinciaResidenza = 'non fornito',
            #     m.luogoNascita = 'non fornito',
            #     m.dataNascita = 'non fornito',
            #     m.indirizzoResidenza = 'non fornito',
            #     m.capResidenza = 'non fornito',
            #     m.cittaResidenza = 'non fornito',
            #     m.nazioneResidenza = 'non fornito',
            #     m.mesiCondanna = 'non fornito',
            #     m.mesiImputati = 'non fornito',
            #     m.mesiTotali = 'non fornito',
            #     m.lng = 'non fornito',
            #     m.lat = 'non fornito',
            #     m.community = 'non fornito'
            # """
            # session.run(query3)

""" query4 ha permesso di prelevare i valori associati alle proprietà sopra facendo un matching in base al nome tra Interlocutore e Individuo """
            # query4 = """
            # MATCH (i:Individuo)
            # WITH i, toLower(i.cognome + ' ' + i.nome) AS fullName
            # MATCH (m:Interlocutore {nome: fullName})
            # SET m.provinciaResidenza = coalesce(i.provinciaResidenza, 'non fornito'),
            #     m.luogoNascita = coalesce(i.luogoNascita, 'non fornito'),
            #     m.dataNascita = coalesce(i.dataNascita, 'non fornito'),
            #     m.indirizzoResidenza = coalesce(i.indirizzoResidenza, 'non fornito'),
            #     m.capResidenza = coalesce(i.capResidenza, 'non fornito'),
            #     m.cittaResidenza = coalesce(i.cittaResidenza, 'non fornito'),
            #     m.nazioneResidenza = coalesce(i.nazioneResidenza, 'non fornito'),
            #     m.mesiCondanna = CASE WHEN i.mesiCondanna IS NULL THEN 'non fornito' ELSE toString(i.mesiCondanna) END,
            #     m.mesiImputati = CASE WHEN i.mesiImputati IS NULL THEN 'non fornito' ELSE toString(i.mesiImputati) END,
            #     m.mesiTotali = CASE WHEN i.mesiTotali IS NULL THEN 'non fornito' ELSE toString(i.mesiTotali) END,
            #     m.lng = CASE WHEN i.lng IS NULL THEN 'non fornito' ELSE toString(i.lng) END,
            #     m.lat = CASE WHEN i.lat IS NULL THEN 'non fornito' ELSE toString(i.lat) END,
            #     m.community = CASE WHEN i.community IS NULL THEN 'non fornito' ELSE toString(i.community) END
            # """
            # session.run(query4)

""" query_conversazioni per la creazione del grafo con nodi etichettati Frase """
            # query_conversazioni = """
            #     MATCH (i:Interlocutore)
            #     WITH i, split(i.info_conversazioni, '}') AS frase
            #     UNWIND frase AS conv
            #     WITH i, trim(conv) + '}' AS conv
            #     WHERE conv <> '}'
            #     CREATE (f:Frasi)
            #     SET f.nome_interlocutore = i.nome, 
            #         f.frase = conv
            #     RETURN f;
            # """
            # session.run(query_conversazioni)

"""query_conversazioni2 permette di creare le diverse proprietà ceh verranno aggiunte a ogni nodo Frase"""
            # query_conversazioni2 = """
            # MATCH (f:Frasi)
            # SET f.ID = split(split(f.frase, "{\nID: ")[1], ",\n")[0],
            #     f.emozione = split(split(f.frase, "emozione: ")[1], ",\n")[0],
            #     f.sentimento = split(split(f.frase, "sentimento: ")[1], ",\n")[0],
            #     f.tipologia = split(split(f.frase, "tipologia: ")[1], ",\n")[0],
            #     f.numero = split(split(f.frase, "numero: ")[1], ",\n")[0],
            #     f.luogo = split(split(f.frase, "luogo: ")[1], ",\n")[0],
            #     f.lista_interlocutori = trim(split(split(f.frase, "lista_interlocutori: ")[1], ",\n")[0]),
            #     f.data_conversazione = split(split(f.frase, "data_conversazione: ")[1], ",\n")[0],
            #     f.orario_conversazione = split(split(f.frase, "orario_conversazione: ")[1], ",\n")[0],
            #     f.frase = split(split(f.frase, "frase: ")[1], "}")[0]
            # """
            # session.run(query_conversazioni2)

""" query2 ha permesso la creazione degli archi (etichattati HaConversato) tra i nodi Interlocutore """
            # query2 = """
            # LOAD CSV WITH HEADERS FROM 'file:////frase_sentiment_emotion_modificato.csv' AS row
            # WITH row, split(row.lista_interlocutori, ', ') AS interlocutori
            # // Gestione di conversazioni con più di due interlocutori
            # WITH row, interlocutori
            # UNWIND range(1, size(interlocutori)) AS j
            # WITH row, interlocutori, interlocutori[0] AS primoInterlocutore, interlocutori[j] AS altroInterlocutore
            # MATCH (interlocutore1:Interlocutore {nome: trim(primoInterlocutore)})
            # MATCH (interlocutore2:Interlocutore {nome: trim(altroInterlocutore)})
            # MERGE (interlocutore1)-[r:HaConversato {ID: toInteger(row.ID), data_conversazione: row.data_conversazione, orario_conversazione: row.orario_conversazione}]->(interlocutore2)
            # ON CREATE SET 
            #     r.tipologia = row.tipologia,
            #     r.numero = toInteger(row.numero),
            #     r.luogo = row.luogo,
            #     r.interlocutori = row.lista_interlocutori,
            #     r.conversazione = [row.frase]
            # ON MATCH SET 
            #     r.conversazione = r.conversazione + [row.frase]
            # RETURN count(*) AS conversations_created
            # """
            # session.run(query2)

""" query per inserire tutte le frasi dette da un interlocutore facendo il matching con il nome """
            # query5= """
            # MATCH (i:Interlocutore)
            # OPTIONAL MATCH (f:Frasi {nome_interlocutore: i.nome})
            # WITH i, COLLECT(f) AS frasi
            # SET i.frasiDette = REDUCE(s = "", frase IN frasi | s + "\n" + "data_conversazione: " + frase.data_conversazione + ",\n" + "orario_conversazione: " + frase.orario_conversazione + ",\n" + "tipologia: " + frase.tipologia + ",\n" + "numero: " + frase.numero + ",\n" + "luogo: " + frase.luogo + ",\n" + "frase: " + frase.frase + ",\n" + "sentimento: " + frase.sentimento + ";\n ")
            # """
            # session.run(query5)

""" query per creazione proprietà emozione predominante in interlocutore con valore iniziale neutrale"""
            # query6 = """
            # MATCH (i:Interlocutore)
            # SET i.emozione_predominante = 'neutrale'
            # RETURN i
            # """
            # session.run(query6)

""" query per assegnazione valore emozione a emozione_predominante in Interlocutore """
            # query7 = """
            # MATCH (i:Interlocutore)
            # OPTIONAL MATCH (f:Frasi {nome_interlocutore: i.nome})
            # WHERE f.sentimento <> 'NEUTRAL'
            # WITH i, f.emozione AS emozione

            # // Step 2: Aggregate the emotions
            # WITH i, collect(emozione) AS emozioni

            # // Step 3: Count the frequency of each emotion
            # UNWIND emozioni AS e
            # WITH i, e, count(e) AS freq
            # ORDER BY freq DESC

            # // Step 4: Get the most frequent emotion
            # WITH i, collect({emotion: e, frequency: freq}) AS emotionFrequencies
            # WITH i, head(emotionFrequencies) AS topEmotion

            # // Step 5: Set the predominant emotion
            # SET i.emozione_predominante = CASE
            #     WHEN topEmotion IS NULL THEN 'NEUTRAL'
            #     ELSE topEmotion.emotion
            # END

            # RETURN i
            # """
            # session.run(query7)

""" query per aggiungere le due nuove proprietà per i reati a ogni interlocutore con valore non fornito """
            # query_reati1 = """
            #     MATCH (i:Interlocutore)
            #     SET i.normeDiRiferimento = 'non fornito',
            #         i.nomeReato = 'non fornito'
            # """
            # session.run(query_reati1)

""" query che ha permesso di assegnare a ogni interlocutore il reato commesso, per chi già presente in individuo"""
            # query_reati2 = """
            #     // Step 1: Retrieve all "Individuo" nodes and their connected "Reato" nodes
            #     MATCH (n:Individuo)-[:Condannato|ImputatoDi]->(r:Reato)
            #     WITH n, COLLECT(r.normeDiRiferimento) AS normeList, COLLECT(r.name) AS nameList

            #     // Step 2: Concatenate the properties
            #     WITH n, REDUCE(s = '', norme IN normeList | s + norme + '; ') AS normeConcat, REDUCE(s = '', name IN nameList | s + name + '; ') AS nameConcat

            #     // Step 3: Find the matching "Interlocutore" node and update its properties
            #     MATCH (i:Interlocutore {nome: toLower(n.cognome + ' ' + n.nome)})
            #     SET i.normeDiRiferimento = normeConcat,
            #         i.nomeReato = nameConcat
            #     RETURN i
            # """
            # session.run(query_reati2)