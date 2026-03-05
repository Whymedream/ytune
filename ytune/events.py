from __future__ import annotations

from abc import ABC
from typing import Any
from typing import Optional
from typing import Tuple
from typing import TYPE_CHECKING

from disnake import Client
from disnake import Guild

from .objects import Track
from .pool import NodePool

if TYPE_CHECKING:
    from .player import Player

__all__ = (
    "YTuneEvent",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackStuckEvent",
    "TrackExceptionEvent",
    "WebSocketClosedPayload",
    "WebSocketClosedEvent",
    "WebSocketOpenEvent",
)


class YTuneEvent(ABC):
    name = "event"
    handler_args: Tuple

    def dispatch(self, bot: Client) -> None:
        bot.dispatch(f"{self.name}", *self.handler_args)


class TrackStartEvent(YTuneEvent):
    name = "track_start"

    __slots__ = (
        "player",
        "track",
    )

    def __init__(self, data: dict, player: Player):
        self.player: Player = player
        self.track: Optional[Track] = self.player._current

        self.handler_args = self.player, self.track

    def __repr__(self) -> str:
        return f"<TrackStartEvent track={self.track.title}>"


class TrackEndEvent(YTuneEvent):
    name = "track_end"

    __slots__ = ("player", "track", "reason")

    def __init__(self, data: dict, player: Player):
        self.player: Player = player
        self.track: Optional[Track] = self.player._ending_track
        self.reason: str = data["reason"]

        self.handler_args = self.player, self.track, self.reason

    def __repr__(self) -> str:
        return (
            f"<TrackEndEvent player={self.player!r} track_id={self.track!r} "
            f"reason={self.reason!r}>"
        )


class TrackStuckEvent(YTuneEvent):
    name = "track_stuck"

    __slots__ = ("player", "track", "threshold")

    def __init__(self, data: dict, player: Player):
        self.player: Player = player
        self.track: Optional[Track] = self.player._ending_track
        self.threshold: float = data["thresholdMs"]

        self.handler_args = self.player, self.track, self.threshold

    def __repr__(self) -> str:
        return (
            f"<TrackStuckEvent player={self.player!r} track={self.track!r} "
            f"threshold={self.threshold!r}>"
        )


class TrackExceptionEvent(YTuneEvent):
    name = "track_exception"

    __slots__ = ("player", "track", "exception")

    def __init__(self, data: dict, player: Player):
        self.player: Player = player
        self.track: Optional[Track] = self.player._ending_track

        self.exception: str = data.get(
            "error",
            "",
        ) or data.get("exception", "")

        self.handler_args = self.player, self.track, self.exception

    def __repr__(self) -> str:
        return f"<TrackExceptionEvent player={self.player!r} exception={self.exception!r}>"


class WebSocketClosedPayload:
    __slots__ = ("guild", "code", "reason", "by_remote")

    def __init__(self, data: dict):
        self.guild: Optional[Guild] = NodePool.get_node().bot.get_guild(int(data["guildId"]))
        self.code: int = data["code"]
        self.reason: str = data["code"]
        self.by_remote: bool = data["byRemote"]

    def __repr__(self) -> str:
        return (
            f"<WebSocketClosedPayload guild={self.guild!r} code={self.code!r} "
            f"reason={self.reason!r} by_remote={self.by_remote!r}>"
        )


class WebSocketClosedEvent(YTuneEvent):
    name = "websocket_closed"

    __slots__ = ("payload",)

    def __init__(self, data: dict, _: Any) -> None:
        self.payload: WebSocketClosedPayload = WebSocketClosedPayload(data)

        self.handler_args = (self.payload,)

    def __repr__(self) -> str:
        return f"<WebsocketClosedEvent payload={self.payload!r}>"


class WebSocketOpenEvent(YTuneEvent):
    name = "websocket_open"

    __slots__ = ("target", "ssrc")

    def __init__(self, data: dict, _: Any) -> None:
        self.target: str = data["target"]
        self.ssrc: int = data["ssrc"]

        self.handler_args = self.target, self.ssrc

    def __repr__(self) -> str:
        return f"<WebsocketOpenEvent target={self.target!r} ssrc={self.ssrc!r}>"
