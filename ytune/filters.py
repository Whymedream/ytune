import collections
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from .exceptions import FilterInvalidArgument

__all__ = (
    "Filter",
    "Equalizer",
    "Timescale",
    "Karaoke",
    "Tremolo",
    "Vibrato",
    "Rotation",
    "Distortion",
    "ChannelMix",
    "LowPass",
)


class Filter:
    __slots__ = ("payload", "tag", "preload")

    def __init__(self, *, tag: str):
        self.payload: Optional[Dict] = None
        self.tag: str = tag
        self.preload: bool = False

    def set_preload(self) -> bool:
        self.preload = True
        return self.preload


class Equalizer(Filter):
    __slots__ = (
        "eq",
        "raw",
    )

    def __init__(self, *, tag: str, levels: list):
        super().__init__(tag=tag)

        self.eq = self._factory(levels)
        self.raw = levels

        self.payload = {"equalizer": self.eq}

    def _factory(self, levels: List[Tuple[Any, Any]]) -> List[Dict]:
        _dict: Dict = collections.defaultdict(int)

        _dict.update(levels)
        data = [{"band": i, "gain": _dict[i]} for i in range(15)]

        return data

    def __repr__(self) -> str:
        return f"EqualizerFilter tag={self.tag} eq={self.eq} raw={self.raw}>"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Equalizer):
            return False

        return self.raw == __value.raw

    @classmethod
    def flat(cls) -> "Equalizer":
        levels = [
            (0, 0.0),
            (1, 0.0),
            (2, 0.0),
            (3, 0.0),
            (4, 0.0),
            (5, 0.0),
            (6, 0.0),
            (7, 0.0),
            (8, 0.0),
            (9, 0.0),
            (10, 0.0),
            (11, 0.0),
            (12, 0.0),
            (13, 0.0),
            (14, 0.0),
        ]
        return cls(tag="flat", levels=levels)

    @classmethod
    def boost(cls) -> "Equalizer":
        levels = [
            (0, -0.075),
            (1, 0.125),
            (2, 0.125),
            (3, 0.1),
            (4, 0.1),
            (5, 0.05),
            (6, 0.075),
            (7, 0.0),
            (8, 0.0),
            (9, 0.0),
            (10, 0.0),
            (11, 0.0),
            (12, 0.125),
            (13, 0.15),
            (14, 0.05),
        ]
        return cls(tag="boost", levels=levels)

    @classmethod
    def metal(cls) -> "Equalizer":
        levels = [
            (0, 0.0),
            (1, 0.1),
            (2, 0.1),
            (3, 0.15),
            (4, 0.13),
            (5, 0.1),
            (6, 0.0),
            (7, 0.125),
            (8, 0.175),
            (9, 0.175),
            (10, 0.125),
            (11, 0.125),
            (12, 0.1),
            (13, 0.075),
            (14, 0.0),
        ]

        return cls(tag="metal", levels=levels)

    @classmethod
    def piano(cls) -> "Equalizer":
        levels = [
            (0, -0.25),
            (1, -0.25),
            (2, -0.125),
            (3, 0.0),
            (4, 0.25),
            (5, 0.25),
            (6, 0.0),
            (7, -0.25),
            (8, -0.25),
            (9, 0.0),
            (10, 0.0),
            (11, 0.5),
            (12, 0.25),
            (13, -0.025),
        ]
        return cls(tag="piano", levels=levels)


class Timescale(Filter):
    __slots__ = ("speed", "pitch", "rate")

    def __init__(self, *, tag: str, speed: float = 1.0, pitch: float = 1.0, rate: float = 1.0):
        super().__init__(tag=tag)

        if speed < 0:
            raise FilterInvalidArgument("Timescale speed must be more than 0.")
        if pitch < 0:
            raise FilterInvalidArgument("Timescale pitch must be more than 0.")
        if rate < 0:
            raise FilterInvalidArgument("Timescale rate must be more than 0.")

        self.speed: float = speed
        self.pitch: float = pitch
        self.rate: float = rate

        self.payload: dict = {
            "timescale": {"speed": self.speed, "pitch": self.pitch, "rate": self.rate},
        }

    @classmethod
    def vaporwave(cls) -> "Timescale":
        return cls(tag="vaporwave", speed=0.8, pitch=0.8)

    @classmethod
    def nightcore(cls) -> "Timescale":
        return cls(tag="nightcore", speed=1.25, pitch=1.3)

    def __repr__(self) -> str:
        return f"<TimescaleFilter tag={self.tag} speed={self.speed} pitch={self.pitch} rate={self.rate}>"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Timescale):
            return False

        return (
            self.speed == __value.speed
            and self.pitch == __value.pitch
            and self.rate == __value.rate
        )


class Karaoke(Filter):
    __slots__ = ("level", "mono_level", "filter_band", "filter_width")

    def __init__(
        self,
        *,
        tag: str,
        level: float = 1.0,
        mono_level: float = 1.0,
        filter_band: float = 220.0,
        filter_width: float = 100.0,
    ):
        super().__init__(tag=tag)

        self.level: float = level
        self.mono_level: float = mono_level
        self.filter_band: float = filter_band
        self.filter_width: float = filter_width

        self.payload: dict = {
            "karaoke": {
                "level": self.level,
                "monoLevel": self.mono_level,
                "filterBand": self.filter_band,
                "filterWidth": self.filter_width,
            },
        }

    def __repr__(self) -> str:
        return (
            f"<KaraokeFilter tag={self.tag} level={self.level} mono_level={self.mono_level} "
            f"filter_band={self.filter_band} filter_width={self.filter_width}>"
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Karaoke):
            return False

        return (
            self.level == __value.level
            and self.mono_level == __value.mono_level
            and self.filter_band == __value.filter_band
            and self.filter_width == __value.filter_width
        )


class Tremolo(Filter):
    __slots__ = ("frequency", "depth")

    def __init__(self, *, tag: str, frequency: float = 2.0, depth: float = 0.5):
        super().__init__(tag=tag)

        if frequency < 0:
            raise FilterInvalidArgument(
                "Tremolo frequency must be more than 0.",
            )
        if depth < 0 or depth > 1:
            raise FilterInvalidArgument(
                "Tremolo depth must be between 0 and 1.",
            )

        self.frequency: float = frequency
        self.depth: float = depth

        self.payload: dict = {
            "tremolo": {
                "frequency": self.frequency,
                "depth": self.depth,
            },
        }

    def __repr__(self) -> str:
        return (
            f"<TremoloFilter tag={self.tag} frequency={self.frequency} depth={self.depth}>"
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Tremolo):
            return False

        return self.frequency == __value.frequency and self.depth == __value.depth


class Vibrato(Filter):
    __slots__ = ("frequency", "depth")

    def __init__(self, *, tag: str, frequency: float = 2.0, depth: float = 0.5):
        super().__init__(tag=tag)

        if frequency < 0 or frequency > 14:
            raise FilterInvalidArgument(
                "Vibrato frequency must be between 0 and 14.",
            )
        if depth < 0 or depth > 1:
            raise FilterInvalidArgument(
                "Vibrato depth must be between 0 and 1.",
            )

        self.frequency: float = frequency
        self.depth: float = depth

        self.payload: dict = {
            "vibrato": {
                "frequency": self.frequency,
                "depth": self.depth,
            },
        }

    def __repr__(self) -> str:
        return (
            f"<VibratoFilter tag={self.tag} frequency={self.frequency} depth={self.depth}>"
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Vibrato):
            return False

        return self.frequency == __value.frequency and self.depth == __value.depth


class Rotation(Filter):
    __slots__ = ("rotation_hertz",)

    def __init__(self, *, tag: str, rotation_hertz: float = 5):
        super().__init__(tag=tag)

        self.rotation_hertz: float = rotation_hertz
        self.payload: dict = {"rotation": {"rotationHz": self.rotation_hertz}}

    def __repr__(self) -> str:
        return f"<RotationFilter tag={self.tag} rotation_hertz={self.rotation_hertz}>"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Rotation):
            return False

        return self.rotation_hertz == __value.rotation_hertz


class ChannelMix(Filter):
    __slots__ = (
        "left_to_left",
        "right_to_right",
        "left_to_right",
        "right_to_left",
    )

    def __init__(
        self,
        *,
        tag: str,
        left_to_left: float = 1,
        right_to_right: float = 1,
        left_to_right: float = 0,
        right_to_left: float = 0,
    ):
        super().__init__(tag=tag)

        if 0 > left_to_left > 1:
            raise ValueError(
                "'left_to_left' value must be more than or equal to 0 or less than or equal to 1.",
            )
        if 0 > right_to_right > 1:
            raise ValueError(
                "'right_to_right' value must be more than or equal to 0 or less than or equal to 1.",
            )
        if 0 > left_to_right > 1:
            raise ValueError(
                "'left_to_right' value must be more than or equal to 0 or less than or equal to 1.",
            )
        if 0 > right_to_left > 1:
            raise ValueError(
                "'right_to_left' value must be more than or equal to 0 or less than or equal to 1.",
            )

        self.left_to_left: float = left_to_left
        self.left_to_right: float = left_to_right
        self.right_to_left: float = right_to_left
        self.right_to_right: float = right_to_right

        self.payload: dict = {
            "channelMix": {
                "leftToLeft": self.left_to_left,
                "leftToRight": self.left_to_right,
                "rightToLeft": self.right_to_left,
                "rightToRight": self.right_to_right,
            },
        }

    def __repr__(self) -> str:
        return (
            f"<ChannelMix tag={self.tag} left_to_left={self.left_to_left} left_to_right={self.left_to_right} "
            f"right_to_left={self.right_to_left} right_to_right={self.right_to_right}>"
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ChannelMix):
            return False

        return (
            self.left_to_left == __value.left_to_left
            and self.left_to_right == __value.left_to_right
            and self.right_to_left == __value.right_to_left
            and self.right_to_right == __value.right_to_right
        )


class Distortion(Filter):
    __slots__ = (
        "sin_offset",
        "sin_scale",
        "cos_offset",
        "cos_scale",
        "tan_offset",
        "tan_scale",
        "offset",
        "scale",
    )

    def __init__(
        self,
        *,
        tag: str,
        sin_offset: float = 0,
        sin_scale: float = 1,
        cos_offset: float = 0,
        cos_scale: float = 1,
        tan_offset: float = 0,
        tan_scale: float = 1,
        offset: float = 0,
        scale: float = 1,
    ):
        super().__init__(tag=tag)

        self.sin_offset: float = sin_offset
        self.sin_scale: float = sin_scale
        self.cos_offset: float = cos_offset
        self.cos_scale: float = cos_scale
        self.tan_offset: float = tan_offset
        self.tan_scale: float = tan_scale
        self.offset: float = offset
        self.scale: float = scale

        self.payload: dict = {
            "distortion": {
                "sinOffset": self.sin_offset,
                "sinScale": self.sin_scale,
                "cosOffset": self.cos_offset,
                "cosScale": self.cos_scale,
                "tanOffset": self.tan_offset,
                "tanScale": self.tan_scale,
                "offset": self.offset,
                "scale": self.scale,
            },
        }

    def __repr__(self) -> str:
        return (
            f"<Distortion tag={self.tag} sin_offset={self.sin_offset} sin_scale={self.sin_scale}> "
            f"cos_offset={self.cos_offset} cos_scale={self.cos_scale} tan_offset={self.tan_offset} "
            f"tan_scale={self.tan_scale} offset={self.offset} scale={self.scale}"
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Distortion):
            return False

        return (
            self.sin_offset == __value.sin_offset
            and self.sin_scale == __value.sin_scale
            and self.cos_offset == __value.cos_offset
            and self.cos_scale == __value.cos_scale
            and self.tan_offset == __value.tan_offset
            and self.tan_scale == __value.tan_scale
            and self.offset == __value.offset
            and self.scale == __value.scale
        )


class LowPass(Filter):
    __slots__ = ("smoothing", "payload")

    def __init__(self, *, tag: str, smoothing: float = 20):
        super().__init__(tag=tag)

        self.smoothing: float = smoothing
        self.payload: dict = {"lowPass": {"smoothing": self.smoothing}}

    def __repr__(self) -> str:
        return f"<LowPass tag={self.tag} smoothing={self.smoothing}>"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, LowPass):
            return False

        return self.smoothing == __value.smoothing
