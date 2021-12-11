import abc
from typing import List, Union, Optional

from step_by_step.common.vector import Vector2f
from step_by_step.game.objects.jobs.action import Action, MoveToAction
from step_by_step.game.objects.jobs.settings import Status, TaskType
from step_by_step.game.objects.world_object import GameObject, WorldObject


class _BaseTask(abc.ABC):
	finished_actions: List[Action]
	unfinished_actions: List[Action]
	current_action: Optional[Action]
	status: Status = Status.PENDING
	task_type: TaskType = TaskType.ONE_OFF

	def update_status(self, new_status: Status):
		self.status = new_status

	@abc.abstractmethod
	def perform(self):
		raise NotImplementedError()


class Task(GameObject, _BaseTask):

	_base_name = 'Task'

	def __str__(self):
		l1 = len(self.unfinished_actions) if self.unfinished_actions else 0
		l2 = len(self.finished_actions) if self.finished_actions else 0
		return f'{super(Task, self).__str__()} ({self.status, l1, l2})'

	def self_destruct_clean_up(self):
		self.finished_actions = None
		self.unfinished_actions = None
		self.current_action = None

	@abc.abstractmethod
	def perform(self):
		raise NotImplementedError()


class MoveToTask(Task):

	_base_name = 'Move To Task'

	def __init__(self, actor: WorldObject, destination: Union[WorldObject, Vector2f]):
		self.finished_actions = []
		self.unfinished_actions = [MoveToAction(actor=actor, destination=destination)]
		self.current_action = None
		super(MoveToTask, self).__init__()

	def perform(self):
		if self.status == Status.PENDING:
			self.update_status(Status.IN_PROGRESS)
		elif self.status == Status.IN_PROGRESS:
			if not self.current_action:
				if len(self.unfinished_actions):
					self.current_action = self.unfinished_actions.pop(0)
				else:
					self.update_status(Status.DONE)
			else:
				if self.current_action.status in [Status.PENDING, Status.IN_PROGRESS]:
					self.current_action.perform()
				elif self.current_action.status in [Status.FAILED, Status.CANCELED]:
					self.update_status(self.current_action.status)
				elif self.current_action.status == Status.DONE:
					self.finished_actions.append(self.current_action)
					self.current_action = None
