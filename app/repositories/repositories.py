from neo4j import GraphDatabase

class InterlocutoreRepository:
    def __init__(self, driver):
        self.driver = driver

    def import_conversations(self, file_path):
        with self.driver.session() as session:
            session.write_transaction(self._import_csv, file_path)

    @staticmethod
    def _import_csv(tx, file_path):
        query = """
        LOAD CSV WITH HEADERS FROM 'file:///' + $file_path AS row
        MERGE (i1:Interlocutore {nome: row.interlocutore1})
        ON CREATE SET i1.emozione = row.emozione1, i1.tipologia = row.tipologia1,
                      i1.luogo = row.luogo1, i1.lista_interlocutori = row.lista_interlocutori1,
                      i1.frase = row.frase1, i1.data_conversazione = row.data_conversazione1,
                      i1.orario_conversazione = row.orario_conversazione1, i1.ID = toInteger(row.ID1),
                      i1.numero = toInteger(row.numero1)
        MERGE (i2:Interlocutore {interlocutore: row.interlocutore2})
        ON CREATE SET i2.emozione = row.emozione2, i2.tipologia = row.tipologia2,
                      i2.luogo = row.luogo2, i2.lista_interlocutori = row.lista_interlocutori2,
                      i2.frase = row.frase2, i2.data_conversazione = row.data_conversazione2,
                      i2.orario_conversazione = row.orario_conversazione2, i2.ID = toInteger(row.ID2),
                      i2.numero = toInteger(row.numero2)
        MERGE (i1)-[r:HaConversato {ID: toInteger(row.conversationID)}]->(i2)
        ON CREATE SET r.tipologia = row.tipologia, r.numero = toInteger(row.numero),
                      r.luogo = row.luogo, r.data_conversazione = row.data_conversazione,
                      r.orario_conversazione = row.orario_conversazione, r.lista_interlocutori = row.lista_interlocutori,
                      r.frase = row.frase
        """
        tx.run(query, file_path=file_path)