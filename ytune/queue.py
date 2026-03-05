from __future__ import annotations

import random
from copy import copy
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

from .enums import LoopMode
from .exceptions import QueueEmpty
from .exceptions import QueueException
from .exceptions import QueueFull
from .objects import Track

__all__ = ("Queue",)


class Queue(Iterable[Track]):
    __slots__ = (
        "max_size",
        "_queue",
        "_overflow",
        "_loop_mode",
        "_current_item",
    )

    def __init__(
        self,
        max_size: Optional[int] = None,
        *,
        overflow: bool = True,
    ):
        self.max_size: Optional[int] = max_size
        self._current_item: Track
        self._queue: List[Track] = []
        self._overflow: bool = overflow
        self._loop_mode: Optional[LoopMode] = None

    def __str__(self) -> str:
        return str(list(f"'{t}'" for t in self))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} max_size={self.max_size} members={self.count}>"

    def __bool__(self) -> bool:
        return bool(self.count)

    def __call__(self, item: Track) -> None:
        self.put(item)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int) -> Track:
        if not isinstance(index, int):
            raise ValueError("'int' type required.'")

        return self._queue[index]

    def __setitem__(self, index: int, item: Track) -> None:
        if not isinstance(index, int):
            raise ValueError("'int' type required.'")

        self.put_at_index(index, item)

    def __delitem__(self, index: int) -> None:
        self._queue.__delitem__(index)

    def __iter__(self) -> Iterator[Track]:
        return self._queue.__iter__()

    def __reversed__(self) -> Iterator[Track]:
        return self._queue.__reversed__()

    def __contains__(self, item: Track) -> bool:
        return item in self._queue

    def __add__(self, other: Iterable[Track]) -> Queue:
        if not isinstance(other, Iterable):
            raise TypeError(
                f"Adding with the '{type(other)}' type is not supported.",
            )

        new_queue = self.copy()
        new_queue.extend(other)
        return new_queue

    def __iadd__(self, other: Union[Iterable[Track], Track]) -> Queue:
        if isinstance(other, Track):
            self.put(other)
            return self

        if isinstance(other, Iterable):
            self.extend(other)
            return self

        raise TypeError(
            f"Adding '{type(other)}' type to the queue is not supported.",
        )

    def _get(self) -> Track:
        return self._queue.pop(0)

    def _drop(self) -> Track:
        return self._queue.pop()

    def _index(self, item: Track) -> int:
        return self._queue.index(item)

    def _put(self, item: Track) -> None:
        self._queue.append(item)

    def _insert(self, index: int, item: Track) -> None:
        self._queue.insert(index, item)

    def _remove(self, item: Track) -> None:
        self._queue.remove(item)

    def _get_random_float(self) -> float:
        return random.random()

    @staticmethod
    def _check_track(item: Track) -> Track:
        if not isinstance(item, Track):
            raise TypeError("Only ytune.Track objects are supported.")

        return item

    @classmethod
    def _check_track_container(cls, iterable: Iterable) -> List[Track]:
        iterable = list(iterable)
        for item in iterable:
            cls._check_track(item)

        return iterable

    @property
    def count(self) -> int:
        return len(self._queue)

    @property
    def is_empty(self) -> bool:
        return not bool(self.count)

    @property
    def is_full(self) -> bool:
        return False if self.max_size is None else self.count >= self.max_size

    @property
    def is_looping(self) -> bool:
        return bool(self._loop_mode)

    @property
    def loop_mode(self) -> Optional[LoopMode]:
        return self._loop_mode

    @property
    def size(self) -> int:
        return len(self._queue)

    def get_queue(self) -> List:
        return self._queue

    def get(self) -> Track:
        if self._loop_mode == LoopMode.TRACK:
            return self._current_item

        if self.is_empty:
            raise QueueEmpty("No items in the queue.")

        if self._loop_mode == LoopMode.QUEUE:
            if not self._current_item or self._current_item not in self._queue:
                if self._queue:
                    item = self._queue[0]
                else:
                    raise QueueEmpty("No items in the queue.")

            if not self._current_item:
                self._current_item = self._queue[0]
                item = self._current_item

            if self._index(self._current_item) == len(self._queue) - 1:
                item = self._queue[0]

            else:
                index = self._index(self._current_item) + 1
                item = self._queue[index]
        else:
            item = self._get()

        self._current_item = item
        return item

    def pop(self) -> Track:
        if self.is_empty:
            raise QueueEmpty("No items in the queue.")

        return self._queue.pop()

    def remove(self, item: Track) -> None:
        return self._remove(self._check_track(item))

    def find_position(self, item: Track) -> int:
        return self._index(self._check_track(item))

    def put(self, item: Track) -> None:
        if self.is_full:
            if not self._overflow:
                raise QueueFull(
                    f"Queue max_size of {self.max_size} has been reached.",
                )

            self._drop()

        return self._put(self._check_track(item))

    def put_at_index(self, index: int, item: Track) -> None:
        if self.is_full:
            if not self._overflow:
                raise QueueFull(
                    f"Queue max_size of {self.max_size} has been reached.",
                )

            self._drop()

        return self._insert(index, self._check_track(item))

    def put_at_front(self, item: Track) -> None:
        return self.put_at_index(0, item)

    def extend(self, iterable: Iterable[Track], *, atomic: bool = True) -> None:
        if atomic:
            iterable = self._check_track_container(iterable)

            if not self._overflow and self.max_size is not None:
                new_len = len(iterable)

                if (new_len + self.count) > self.max_size:
                    raise QueueFull(
                        f"Queue has {self.count}/{self.max_size} items, "
                        f"cannot add {new_len} more.",
                    )

        for item in iterable:
            self.put(item)

    def copy(self) -> Queue:
        new_queue = self.__class__(max_size=self.max_size)
        new_queue._queue = copy(self._queue)

        return new_queue

    def clear(self) -> None:
        self._queue.clear()

    def set_loop_mode(self, mode: LoopMode) -> None:
        self._loop_mode = mode
        if self._loop_mode == LoopMode.QUEUE:
            try:
                index = self._index(self._current_item)
            except ValueError:
                index = 0
            if self._current_item not in self._queue:
                self._queue.insert(index, self._current_item)
            self._current_item = self._queue[index]

    def disable_loop(self) -> None:
        if not self._loop_mode:
            raise QueueException("Queue loop is already disabled.")

        if self._loop_mode == LoopMode.QUEUE:
            index = self.find_position(self._current_item) + 1
            self._queue = self._queue[index:]

        self._loop_mode = None

    def shuffle(self) -> None:
        return random.shuffle(self._queue)

    def clear_track_filters(self) -> None:
        for track in self._queue:
            track.filters = None

    def jump(self, item: Track) -> None:
        if self._loop_mode == LoopMode.TRACK:
            raise QueueException("Jumping the queue whilst looping a track is not allowed.")

        index = self.find_position(item)
        if self._loop_mode == LoopMode.QUEUE:
            self._current_item = self._queue[index - 1]
        else:
            new_queue = self._queue[index : self.size]
            self._queue = new_queue
