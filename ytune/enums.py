import re
from enum import Enum
from enum import IntEnum

__all__ = (
    "SearchType",
    "TrackType",
    "PlaylistType",
    "NodeAlgorithm",
    "LoopMode",
    "RouteStrategy",
    "RouteIPType",
    "URLRegex",
    "LogLevel",
)


class SearchType(Enum):
    ytsearch = "ytsearch"
    ytmsearch = "ytmsearch"
    scsearch = "scsearch"
    ymsearch = "ymsearch"
    spsearch = "spsearch"
    amsearch = "amsearch"
    dzsearch = "dzsearch"
    vksearch = "vksearch"
    tdsearch = "tdsearch"
    qbsearch = "qbsearch"

    def __str__(self) -> str:
        return self.value


class TrackType(Enum):
    YOUTUBE = "youtube"
    SOUNDCLOUD = "soundcloud"
    HTTP = "http"
    LOCAL = "local"
    OTHER = "other"

    @classmethod
    def _missing_(cls, _: object) -> "TrackType":
        return cls.OTHER

    def __str__(self) -> str:
        return self.value


class PlaylistType(Enum):
    YOUTUBE = "youtube"
    SOUNDCLOUD = "soundcloud"
    OTHER = "other"

    @classmethod
    def _missing_(cls, _: object) -> "PlaylistType":
        return cls.OTHER

    def __str__(self) -> str:
        return self.value


class NodeAlgorithm(Enum):
    by_ping = "BY_PING"
    by_players = "BY_PLAYERS"

    def __str__(self) -> str:
        return self.value


class LoopMode(Enum):
    TRACK = "track"
    QUEUE = "queue"

    def __str__(self) -> str:
        return self.value


class RouteStrategy(Enum):
    ROTATE_ON_BAN = "RotatingIpRoutePlanner"
    LOAD_BALANCE = "BalancingIpRoutePlanner"
    NANO_SWITCH = "NanoIpRoutePlanner"
    ROTATING_NANO_SWITCH = "RotatingNanoIpRoutePlanner"


class RouteIPType(Enum):
    IPV4 = "Inet4Address"
    IPV6 = "Inet6Address"


class URLRegex:
    DISCORD_MP3_URL = re.compile(
        r"https?://cdn.discordapp.com/attachments/(?P<channel_id>[0-9]+)/"
        r"(?P<message_id>[0-9]+)/(?P<file>[a-zA-Z0-9_.]+)+",
    )

    YOUTUBE_URL = re.compile(
        r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))"
        r"(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$",
    )

    YOUTUBE_PLAYLIST_URL = re.compile(
        r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))/playlist\?list=.*",
    )

    YOUTUBE_TIMESTAMP = re.compile(
        r"(?P<video>^.*?)(\?t|&start)=(?P<time>\d+)?.*",
    )

    AM_URL = re.compile(
        r"https?://music.apple.com/(?P<country>[a-zA-Z]{2})/"
        r"(?P<type>album|playlist|song|artist)/(?P<name>.+)/(?P<id>[^?]+)",
    )

    AM_SINGLE_IN_ALBUM_REGEX = re.compile(
        r"https?://music.apple.com/(?P<country>[a-zA-Z]{2})/(?P<type>album|playlist|song|artist)/"
        r"(?P<name>.+)/(?P<id>.+)(\?i=)(?P<id2>.+)",
    )

    SOUNDCLOUD_URL = re.compile(
        r"((?:https?:)?\/\/)?((?:www|m)\.)?soundcloud.com\/.*/.*",
    )

    SOUNDCLOUD_PLAYLIST_URL = re.compile(
        r"^(https?:\/\/)?(www.)?(m\.)?soundcloud\.com\/.*/sets/.*",
    )

    SOUNDCLOUD_TRACK_IN_SET_URL = re.compile(
        r"^(https?:\/\/)?(www.)?(m\.)?soundcloud\.com/[a-zA-Z0-9-._]+/[a-zA-Z0-9-._]+(\?in)",
    )

    LAVALINK_SEARCH = re.compile(r"(?P<type>ytm?|sc)search:")

    BASE_URL = re.compile(r"https?://(?:www\.)?.+")


class LogLevel(IntEnum):

    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    CRITICAL = 50

    @classmethod
    def from_str(cls, level_str):
        try:
            return cls[level_str.upper()]
        except KeyError:
            raise ValueError(f"No such log level: {level_str}")
