"""Mixin for APIs with task support."""

from collections.abc import Callable
from typing import TypeVar

from ..models.base import BaseTaskDetails
from ..utils.tasks import TaskPoller, wait_for_task

T = TypeVar("T", bound=BaseTaskDetails)


class TaskAPIMixin:
    """Mixin for APIs that work with async tasks."""

    def _wait_for_task(
        self,
        task_id: str,
        check_fn: Callable[[str], T],
        timeout: int = 300,
        interval: int = 2,
        on_progress: Callable[[T], None] | None = None,
    ) -> T:
        """
        Wait for task to complete.

        Args:
            task_id: Task ID to monitor
            check_fn: Function to check task status
            timeout: Maximum wait time in seconds
            interval: Initial polling interval in seconds
            on_progress: Optional progress callback

        Returns:
            Completed task details

        Raises:
            TaskTimeoutError: If timeout exceeded
            TaskFailedError: If task failed
        """
        return wait_for_task(
            check_fn=check_fn,
            task_id=task_id,
            timeout=timeout,
            interval=interval,
            on_progress=on_progress,
        )

    def _create_poller(
        self,
        task_id: str,
        check_fn: Callable[[str], T],
        timeout: int = 300,
        interval: int = 2,
        backoff_factor: float = 1.5,
        max_interval: int = 30,
    ) -> TaskPoller[T]:
        """
        Create task poller for manual control.

        Args:
            task_id: Task ID to monitor
            check_fn: Function to check task status
            timeout: Maximum wait time in seconds
            interval: Initial polling interval in seconds
            backoff_factor: Multiplier for exponential backoff
            max_interval: Maximum polling interval in seconds

        Returns:
            TaskPoller instance for manual control

        Example:
            >>> poller = api._create_poller("task-123", api.get_task_status)
            >>> # Do other work...
            >>> result = poller.wait()
        """
        return TaskPoller(
            check_fn=check_fn,
            task_id=task_id,
            timeout=timeout,
            interval=interval,
            backoff_factor=backoff_factor,
            max_interval=max_interval,
        )
