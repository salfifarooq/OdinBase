from __future__ import annotations

from .sub import rand_gen


def main_func(num: int) -> dict[str, int]:
    if num < 0:
        raise ValueError("must not be < 0")
    return rand_gen(num=num)
