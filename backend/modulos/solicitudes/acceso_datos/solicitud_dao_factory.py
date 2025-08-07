from abc import ABC, abstractmethod

class SolicitudDAOFactory(ABC):
    @abstractmethod
    def crear_dao(self):
        pass
