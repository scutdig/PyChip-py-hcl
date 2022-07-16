from abc import ABC, abstractmethod


class FirrtlNode(ABC):
    """Intermediate Representation"""

    @abstractmethod
    def serialize(self) -> str:
        ...

    @abstractmethod
    def verilog_serialize(self) -> str:
        ...
