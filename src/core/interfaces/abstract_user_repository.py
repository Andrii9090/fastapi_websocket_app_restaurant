from abc import ABC

from core.interfaces.abstract_repository import AbstractRepository


class AbstractUserRepository(AbstractRepository, ABC):
    def get_by_email(self, email: str):
        raise NotImplementedError

    def set_inactive(self, user_id: int):
        raise NotImplementedError