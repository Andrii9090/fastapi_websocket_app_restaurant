from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def create(self, obj):
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, obj) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, limit, offset, where, order_by):
        raise NotImplementedError
