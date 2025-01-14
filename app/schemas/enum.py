from enum import Enum

class UType(Enum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    GUEST = 'guest'
    ADMIN = 'admin'

class QType(Enum):
    """Korean -> 질문 한국어, 답변 영어"""
    KOREAN= 'korean'
    ENGLISH= 'english'

class Difficulty(Enum):
    EASY = 'easy'
    MODERATE = 'moderate'
    HARD = 'hard'

class Tag(Enum):
    NOUN = 'noun'  # 명사
    PRONOUN = 'pronoun'  # 대명사
    VERB = 'verb'  # 동사
    ADJECTIVE = 'adjective'  # 형용사
    ADVERB = 'adverb'  # 부사
    PREPOSITION = 'preposition'  # 전치사
    CONJUNCTION = 'conjunction'  # 접속사
    INTERJECTION = 'interjection'  # 감탄사

    UNDECIDED = 'undecided'

class APIStatus(Enum):
    SUCCESS = 20000
    FAIL = 50001
    ERROR = 50000


class StoreSearchOption(Enum):
    ALL = 'all'
    META = 'meta'
    VALUE = 'value'