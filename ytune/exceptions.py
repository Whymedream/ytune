__all__ = (
    "YTuneException",
    "NodeException",
    "NodeCreationError",
    "NodeConnectionFailure",
    "NodeConnectionClosed",
    "NodeRestException",
    "NodeNotAvailable",
    "NoNodesAvailable",
    "TrackInvalidPosition",
    "TrackLoadError",
    "FilterInvalidArgument",
    "FilterTagInvalid",
    "FilterTagAlreadyInUse",
    "QueueException",
    "QueueFull",
    "QueueEmpty",
    "LavalinkVersionIncompatible",
)


class YTuneException(Exception):
    pass


class NodeException(Exception):
    pass


class NodeCreationError(NodeException):
    pass


class NodeConnectionFailure(NodeException):
    pass


class NodeConnectionClosed(NodeException):
    pass


class NodeRestException(NodeException):
    pass


class NodeNotAvailable(YTuneException):
    pass


class NoNodesAvailable(YTuneException):
    pass


class TrackInvalidPosition(YTuneException):
    pass


class TrackLoadError(YTuneException):
    pass


class FilterInvalidArgument(YTuneException):
    pass


class FilterTagInvalid(YTuneException):
    pass


class FilterTagAlreadyInUse(YTuneException):
    pass


class QueueException(Exception):
    pass


class QueueFull(QueueException):
    pass


class QueueEmpty(QueueException):
    pass


class LavalinkVersionIncompatible(YTuneException):
    pass
