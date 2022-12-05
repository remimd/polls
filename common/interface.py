from common.injection import Injectable
from common.patterns import Singleton


class Interface(Singleton, metaclass=Injectable):
    pass
