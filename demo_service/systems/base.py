from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demo_service.systems import HackspaceSystems

class SystemBase:
    def __init__(self, hs: HackspaceSystems):
        self.hs = hs