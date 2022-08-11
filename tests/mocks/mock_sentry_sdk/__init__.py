from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional

# Not sentry-sdk, but just enough stubbing to make the tests work


class Client:
    def __init__(self, *args: Any, **options: str) -> None:
        self.dsn = options.get("dsn")


class Hub:
    current: Optional[Hub] = None

    def __init__(self, client: Optional[Client] = None) -> None:
        self.client = client


Hub.current = Hub()
