from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from np_lang.stem.itrstem import IterativeStemmer
from np_lang.tokenize.tokenizer import Tokenizer
from np_lang.rmvstopwords import StopWordRemover

"""
 >>> from np_lang.vectorizer import VectorSpaceModel
 >>>  d1 = "त्यो घर रातो छ"
 >>>  d2 = "यो निलो कलम हो"
 >>>  d3 = "भाईको घर हो"
 >>>  documents = [d1, d2, d3]
 
 >>>  vector_space_model = VectorSpaceModel(documents)

 >>>  print (vector_space_model)
        
        <VectorSpaceModel with vocabulary {'निलो': 2, 'कलम': 0, 'रातो': 4, 'घर': 1, 'भाई': 3} >

 >>>  print(vector_space_model.tf)
      
      (0, 4)	1
      (0, 1)	1
      (1, 0)	1
      (1, 2)	1
      (2, 3)	1
      (2, 1)	1
            
  >>>  print(vector_space_model.tf_idf)
  
      (0, 1)	0.605348508106
      (0, 4)	0.795960541568
      (1, 2)	0.707106781187
      (1, 0)	0.707106781187
      (2, 1)	0.605348508106
      (2, 3)	0.795960541568
 
 >>>  print(vector_space_model.vocabulary())

        {'निलो': 2, 'कलम': 0, 'रातो': 4, 'घर': 1, 'भाई': 3}
 
 >>>  print(vector_space_model.tf_matrix())
        
         [[0 1 0 0 1]
          [1 0 1 0 0]
          [0 1 0 1 0]]
         
 >>>  print(vector_space_model.idf_matrix())
        
        [ 1.69314718  1.28768207  1.69314718  1.69314718  1.69314718]
             
 >>>  print(vector_space_model.tf_idf_matrix())
        [[ 0.          0.60534851  0.          0.          0.79596054]
         [ 0.70710678  0.          0.70710678  0.          0.        ]
         [ 0.          0.60534851  0.          0.79596054  0.        ]]
 
 >>>  print(vector_space_model.document_similarity())
        [[ 1.          0.          0.36644682]
         [ 0.          1.          0.        ]
         [ 0.36644682  0.          1.        ]] 
"""


class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        stemmer = IterativeStemmer()
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (stemmer.stem(w) for w in analyzer(doc))


class VectorSpaceModel:
    def __init__(self, documents):
        self.documents = documents
        self.vectorizer = StemmedCountVectorizer()
        self.tf = None
        self.tf_idf = None
        self.__tfidf = None

    def __repr__(self):
        return "<VectorSpaceModel with vocabulary " + str(self.vocabulary()) + " >"

    def __compute_tf(self):
        if not self.documents:
            raise Exception("Documents cannot be empty")
        self.vectorizer = StemmedCountVectorizer(stop_words=StopWordRemover().get_stopwords(),
                                                 tokenizer=lambda text: Tokenizer().word_tokenize(text=text),
                                                 analyzer='word')
        self.tf = self.vectorizer.fit_transform(self.documents)

    def compute_tf_idf(self):
        self.__compute_tf()
        self.__tfidf = TfidfTransformer(norm="l2")
        self.__tfidf.fit(self.tf)
        self.tf_idf = self.__tfidf.transform(self.tf)

    def vocabulary(self):
        try:
            return self.vectorizer.vocabulary_
        except Exception:
            return {}

    def tf_matrix(self):
        if self.tf is not None:
            return self.tf.todense()
        return []

    def idf_matrix(self):
        if self.__tfidf is not None:
            return self.__tfidf.idf_
        return []

    def tf_idf_matrix(self):
        if self.tf_idf is not None:
            return self.tf_idf.todense()
        return []

    def document_similarity(self):
        if self.tf_idf is not None:
            return cosine_similarity(self.tf_idf)
        raise Exception("Compute tf idf first")
