from typing import Any, List, Self, Type, TypeVar
from abc import  ABC
from sqlmodel import SQLModel, Session, col, select
from common.utils.model_graphql_utils import model_to_strawberry
from core.database import DB_ENGINE
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)
U = TypeVar("U")

class BaseManager(ABC):
    """
    Contains base operations for managing database models
    """
    def __init__(self, model_class: Type[T], gql_type: Type[U], fields: List[str]) -> None: # type: ignore
        self.value: model_class
        self.bulk_values: List[model_class]
        self.__model_class = model_class
        self.gql_type = gql_type
        self.gql: U
        self.bulk_gql: List[U]
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
            self.value = new_item
            for field in self.__fields:
                getattr(self.value, field)
        self.__to_gql()
        return self


    def get(self, **kwargs) -> Self:
        """
        Performs a select operations for a specific item
        """
        if not any(kwargs.values()):
            raise ValueError("At least one argument must be passed")

        with Session(DB_ENGINE) as session:
            statement = select(self.__model_class)
            for key, value in kwargs.items():
                if value is not None:
                    statement = statement.where(getattr(self.__model_class, key)==value)
            value = session.exec(statement).one()
            self.value = value
            for relationship in self.__model_class.__sqlmodel_relationships__:
                getattr(self.value, relationship)
            print({"the_fields": self.__model_class.__sqlmodel_relationships__})
            self.__to_gql()
            return self


    def filter(self, equals: dict|None=None, ins: dict|None=None, offset: int|None=None, limit: int|None=None) -> Self:
        """
        Filters and returns all matches based on the passed arguments
        """
        if not equals and not ins:
            raise ValueError("equals or ins arguments must be passed")

        with Session(DB_ENGINE) as session:
            statement = select(self.__model_class)

            if equals and any(equals.values()):
                for key, value in equals.items():
                    statement = statement.where(getattr(self.__model_class, key)==value)

            if ins and any(ins.values()):
                for key, value in ins.items():
                    statement = statement.where(col(getattr(self.__model_class, key)).in_(value))

            for relationship in self.__model_class.__sqlmodel_relationships__:
                statement = statement.join(getattr(self.__model_class, relationship))

            if offset: statement = statement.offset(offset)
            if limit: statement = statement.limit(limit)
                
            items = session.exec(statement).all()
            self.bulk_values = items
            self.bulk_gql = list(map(lambda item: self.__parse_gql(item), items))
        return self


    def all(self, offset:int|None=None, limit:int|None=None) -> Self:
        """
        Returns all columns of a database table
        """
        with Session(DB_ENGINE) as session:
            statement = select(self.__model_class)
            for relationship in self.__model_class.__sqlmodel_relationships__:
                statement = statement.join(getattr(self.__model_class, relationship))
            if offset: statement = statement.offset(offset)
            if limit: statement = statement.limit(limit)
            items = session.exec(statement).all()
            self.bulk_values = items
            self.bulk_gq = list(map(lambda item: self.__parse_gql(item), items))
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


    def __parse_gql(self, instance: Any|None=None):
        """
        Returns the graphql representation for this model
        """
        return model_to_strawberry(
                obj=instance if instance else self.value,
                fields=self.__fields,
                strawberry=self.gql_type,
                model=self.__model_class)

    def __to_gql(self):
        self.gql = self.__parse_gql()
        return self
