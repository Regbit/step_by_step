import abc

from typing import Union

from step_by_step.game.objects.jobs.settings import Status
from step_by_step.game.objects.world_object import GameObject, WorldObject
from step_by_step.common.vector import Vector2f


class _BaseAction(abc.ABC):
	status: Status = Status.PENDING
	duration_sec: int = -1

	def update_status(self, new_status: Status):
		self.status = new_status

	@abc.abstractmethod
	def perform(self):
		raise NotImplementedError()


class Action(GameObject, _BaseAction):

	@abc.abstractmethod
	def self_destruct_clean_up(self):
		raise NotImplementedError()

	def __str__(self):
		return f'{super(Action, self).__str__()} ({self.status})'


class MoveToAction(Action):

	def self_destruct_clean_up(self):
		self.actor = None
		self.destination = None

	def __init__(self, actor: WorldObject, destination: Union[WorldObject, Vector2f]):
		super(MoveToAction, self).__init__()
		self.actor = actor
		self.destination = destination
		self.target_proximity = (actor.size.x + destination.size.x) / 2

	def perform(self):
		if self.status.PENDING:
			self.update_status(Status.IN_PROGRESS)
		if self.status.IN_PROGRESS:
			try:
				start: Vector2f = self.actor.world_pos
				finish: Vector2f = self.destination

				if not isinstance(self.destination, Vector2f):
					finish = self.destination.world_pos

				if start.dist(finish) > self.target_proximity:
					# rotate actor
					self.actor.rotate_towards(finish)
					# move actor
					self.actor.move_towards(finish)
				else:
					self.update_status(Status.DONE)
			except Exception as e:
				self.update_status(Status.FAILED)
				raise e
