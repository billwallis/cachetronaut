import datetime
import pathlib
from types import SimpleNamespace

from cachetronaut import file_cache

NOW = datetime.datetime.now()


def test__file_cache__can_cache_to_file_and_be_reused(tmp_path: pathlib.Path):
    cache_path = tmp_path / "foo.pickle"
    cache_data = SimpleNamespace(
        salutation="hello",
        is_awesome=True,
    )
    foo_calls = []

    @file_cache(
        filepath=cache_path,
        expiration=datetime.timedelta(hours=1),
    )
    def foo():
        # some expensive computation
        foo_calls.append(1)  # Is there a better way to have a mutatable counter?!
        return cache_data

    # Initially, the cache doesn't exist
    assert not cache_path.exists()

    # Then, it's created and used
    assert foo() == cache_data
    assert sum(foo_calls) == 1
    assert cache_path.exists()

    # Calling the cached function again doesn't actually run it
    assert foo() == cache_data
    assert sum(foo_calls) == 1


def test__file_cache__will_regenerate_cache_if_expired(tmp_path: pathlib.Path):
    cache_path = tmp_path / "foo.pickle"
    cache_data = "bar"
    foo_calls = []

    @file_cache(
        filepath=cache_path,
        expiration=datetime.timedelta(seconds=0),
    )
    def foo():
        foo_calls.append(1)
        return cache_data

    # Initially, the cache doesn't exist
    assert not cache_path.exists()

    # Then, it's created and used
    assert foo() == cache_data
    assert sum(foo_calls) == 1
    assert cache_path.exists()

    # Calling the cached function again runs it because the cache expired
    assert foo() == cache_data
    assert sum(foo_calls) == 2
