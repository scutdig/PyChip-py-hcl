from abc import ABC, abstractmethod


class FirrtlNode(ABC):
    """Intermediate Representation"""

    @abstractmethod
    def serialize(self) -> str:
        ...