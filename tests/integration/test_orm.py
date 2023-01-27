import pytest

pytestmark = pytest.mark.usefixtures("mappers")


def test_session_factory(postgres_session_factory):
    postgres_session_factory()
