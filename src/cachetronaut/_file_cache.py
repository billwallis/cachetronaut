import dataclasses
import datetime
import functools
import logging
import pathlib
import pickle
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__file__)

HERE = pathlib.Path(__file__).resolve().parent

# TODO: Add ability to invalidate caches


@dataclasses.dataclass
class _PickleCache:
    expires_at: datetime.datetime
    data: Any


def _pickle_cache[T](
    expr: Callable[[], T],
    pickle_path: pathlib.Path,
    expiration: datetime.timedelta,
) -> T:
    if pickle_path.exists():
        logger.debug(f"pickle '{pickle_path}' exists")
        with open(pickle_path, "rb") as f:
            unpickled: _PickleCache = pickle.load(f)
        if unpickled.expires_at > datetime.datetime.now():
            logger.debug(
                f"reusing pickle '{pickle_path}' (expires {unpickled.expires_at})"
            )
            return unpickled.data
        logger.debug(
            f"pickle '{pickle_path}' has expired (expired at {unpickled.expires_at})"
        )

    logger.debug(f"generating pickle '{pickle_path}'")
    data = expr()
    to_pickle = _PickleCache(
        expires_at=datetime.datetime.now() + expiration,
        data=data,
    )
    with open(pickle_path, "wb") as f:
        pickle.dump(to_pickle, f, pickle.HIGHEST_PROTOCOL)

    return data


def file_cache[T](
    filepath: pathlib.Path,
    expiration: datetime.timedelta,
) -> T:
    def pickle_cache_dec(func: Callable[[Any, ...], T]) -> Callable[[Any, ...], T]:
        @functools.wraps(func)
        def pickle_cache_dec_impl(*args, **kwargs) -> T:
            return _pickle_cache(
                expr=functools.partial(func, *args, **kwargs),
                pickle_path=filepath,
                expiration=expiration,
            )

        return pickle_cache_dec_impl

    return pickle_cache_dec
