from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

class TopicModeler:
    def __init__(self):
        self.embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        self.model = BERTopic(
            embedding_model=self.embedding_model,
            language='spanish',
            nr_topics=8,
            min_topic_size=10
        )
    
    def entrenar(self, textos):
        temas, _ = self.model.fit_transform(textos)
        info_temas = self.model.get_topic_info()
        
        factores = []
        for _, row in info_temas.iterrows():
            if row['Topic'] != -1:
                palabras = self.model.get_topic(row['Topic'])
                factores.append({
                    'id': row['Topic'],
                    'palabras_clave': [p[0] for p in palabras[:10]],
                    'menciones': row['Count']
                })
        return factores