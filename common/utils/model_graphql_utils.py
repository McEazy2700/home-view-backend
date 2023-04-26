from typing import List, Type, TypeVar

T = TypeVar("T")
U = TypeVar("U")

def model_to_strawberry(strawberry: Type[T], model: Type[U], obj: U, fields: List[str]) -> T:
    """
    Converts model instance to graphql object type
    """
    kwargs = {}
    model_keys = []

    for key in model.__dict__.keys():
        if key[0] != "_" and key in fields:
            model_keys.append(key)

    for key in model_keys: kwargs[key] = getattr(obj, key) if hasattr(obj, key) else None
    strawberry_instance: strawberry  = strawberry(**kwargs)
    return strawberry_instance
