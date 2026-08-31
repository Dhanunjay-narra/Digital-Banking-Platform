"""Asynchronous In-Memory Event Bus for Domain Event Pub/Sub."""

import asyncio
from typing import Callable, Dict, List, Any
from datetime import datetime, timezone


class DomainEvent:
    def __init__(self, event_name: str, payload: Dict[str, Any], correlation_id: str = ""):
        self.event_name = event_name
        self.payload = payload
        self.correlation_id = correlation_id
        self.timestamp = datetime.now(timezone.utc).isoformat()


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, handler: Callable):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

    def publish(self, event: DomainEvent):
        handlers = self._subscribers.get(event.event_name, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(event))
                else:
                    handler(event)
            except Exception as e:
                # Log event handler failure without halting publishing pipeline
                print(f"[EventBus Error] Failed executing handler for {event.event_name}: {e}")


event_bus = EventBus()
