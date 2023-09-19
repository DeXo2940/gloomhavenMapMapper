from __future__ import annotations
import abc

from .api_method import ApiMethod


class GloomhavenApi(abc.ABC):
    @abc.abstractmethod
    def get_endpoint(self) -> str:
        pass

    @abc.abstractmethod
    def get_path(self) -> str:
        pass

    @abc.abstractmethod
    def get_avaliable_methods(
        self,
    ) -> list[ApiMethod]:
        pass
