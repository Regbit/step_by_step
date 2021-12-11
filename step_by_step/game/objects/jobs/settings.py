from enum import Enum


class Status(Enum):
	PENDING = 1
	IN_PROGRESS = 2
	DONE = 3
	FAILED = 4
	CANCELED = 5


class TaskType(Enum):
	ONE_OFF = 1
	REPEATABLE = 2
