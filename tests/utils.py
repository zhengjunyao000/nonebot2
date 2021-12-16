from pathlib import Path
from typing import TYPE_CHECKING, Set, Type, Optional

import pytest
from pydantic import create_model

if TYPE_CHECKING:
    from nonebot.plugin import Plugin
    from nonebot.adapters import Event, Message


def make_fake_event(
    _type: str = "message",
    _name: str = "test",
    _description: str = "test",
    _user_id: str = "test",
    _session_id: str = "test",
    _message: Optional["Message"] = None,
    _to_me: bool = True,
    **fields,
) -> Type["Event"]:
    from nonebot.adapters import Event

    _Fake = create_model("_Fake", __base__=Event, **fields)

    class FakeEvent(_Fake):
        def get_type(self) -> str:
            return _type

        def get_event_name(self) -> str:
            return _name

        def get_event_description(self) -> str:
            return _description

        def get_user_id(self) -> str:
            return _user_id

        def get_session_id(self) -> str:
            return _session_id

        def get_message(self) -> "Message":
            if _message is not None:
                return _message
            raise NotImplementedError

        def is_tome(self) -> bool:
            return _to_me

        class Config:
            extra = "forbid"

    return FakeEvent


@pytest.fixture
def load_plugin(nonebug_init: None) -> Set["Plugin"]:
    import nonebot

    return nonebot.load_plugins(str(Path(__file__).parent / "plugins"))