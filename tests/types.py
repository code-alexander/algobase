"""Type aliases for test parameters."""

from typing import Any, TypeAlias

# FixtureValue: TypeAlias = str | int | bool | bytes | None
# FixtureDict: TypeAlias = dict[
#     str, FixtureValue | list[FixtureValue] | dict[str, FixtureValue]
# ]

FixtureDict: TypeAlias = dict[str, Any]
