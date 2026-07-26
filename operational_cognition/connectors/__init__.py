"""External-system connector adapters governed by AKOS Operational Cognition.

Connector modules are intentionally not imported eagerly so each adapter remains
independently executable with ``python -m`` and unavailable providers do not
break package discovery.
"""

__all__: list[str] = []
