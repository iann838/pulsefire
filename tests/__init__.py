from typing import Callable
import inspect
import functools

import typeguard
from pulsefire.base import Client
from pulsefire.clients import (
    CDragonClient,
    DDragonClient,
    MarlonAPIClient,
    MerakiCDNClient,
    RiotAPIClient,
)


def typechecked_client_responses(client_cls: type[Client]):
    def typechecked_return[**P, R](func: Callable[P, R]) -> Callable[P, R]:
        if "return" not in func.__annotations__:
            return func
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            response = await func(*args, **kwargs)
            typeguard.check_type(response, func.__annotations__["return"])
            return response
        return wrapper

    if not issubclass(client_cls, Client):
        raise TypeError(f"{client_cls} is not a pulsefire client")
    for name in dir(client_cls):
        if inspect.iscoroutinefunction(member := getattr(client_cls, name)):
            setattr(client_cls, name, typechecked_return(member))


typechecked_client_responses(CDragonClient)
typechecked_client_responses(DDragonClient)
typechecked_client_responses(MarlonAPIClient)
typechecked_client_responses(MerakiCDNClient)
typechecked_client_responses(RiotAPIClient)
