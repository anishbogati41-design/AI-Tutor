from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TopicRecord:
    id: int
    name: str
    parent_topic_id: int | None
    description: str
