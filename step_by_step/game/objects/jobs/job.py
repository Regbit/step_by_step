import abc
import typing

from step_by_step.game.objects.jobs.task import Task
from step_by_step.game.objects.world_object import GameObject


class _BaseJob(abc.ABC):

	_tasks: typing.OrderedDict[str, Task]


class Job(GameObject, _BaseJob):
	pass