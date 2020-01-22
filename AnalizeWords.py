from konlpy.tag import Kkma
from konlpy.utils import pprint


class AnalizeWords:
    def test(self, sentence):
        kkma = Kkma()
        pprint(kkma.sentences(sentence))

