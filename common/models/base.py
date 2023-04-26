from typing import Any, List, Self, Type, TypeVar
from abc import abstractmethod, ABC
from sqlmodel import Session
from common.utils.model_graphql_utils import model_to_strawberry
from core.database import DB_ENGINE

T = TypeVar("T")
U = TypeVar("U")

class BaseManager(ABC):
    """
    Contains base operations for managing database models
    """
    def __init__(self, model_class: Type[T], gql_type: Type[U], fields: List[str]) -> None: # type: ignore
        self.value: model_class
        self.__value: model_class
        self.__model_class = model_class
        self.__gql = gql_type
        self.__fields = fields

    def new(self, **kwargs) -> Self:
        """
        Performs a create operations for this model
        """
        with Session(DB_ENGINE) as session:
            new_item = self.__model_class(**kwargs)
            session.add(new_item)
            for field in self.__fields:
                getattr(new_item, field)
            session.commit()
            session.refresh(new_item)
            self.__value = new_item
            for field in self.__fields:
                getattr(self.__value, field)
        return self

    @abstractmethod
    def get(self) -> Self:
        """
        Performs a select operations for a specific item
        """
        return self

    def delete(self, instance: Any|None=None):
        """
        Performs a delete operation on self
        """
        if not instance and not hasattr(self, "value"):
            raise ValueError("instance to be deleted is required")
        with Session(DB_ENGINE) as session:
            if instance:
                session.delete(instance)
            else:
                session.delete(self.value)
            session.commit()

    def gql(self):
        """
        Returns the graphql representation for this model
        """
        return model_to_strawberry(
                obj=self.__value,
                fields=self.__fields,
                strawberry=self.__gql,
                model=self.__model_class)
