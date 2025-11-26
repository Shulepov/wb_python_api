"""Utilities for working with async tasks."""

import time
from collections.abc import Callable
from typing import Generic, TypeVar

from ..models.base import BaseTaskDetails

T = TypeVar("T", bound=BaseTaskDetails)


class TaskTimeoutError(Exception):
    """Task execution timeout error."""

    def __init__(self, task_id: str, timeout: float):
        self.task_id = task_id
        self.timeout = timeout
        super().__init__(f"Task {task_id} timeout after {timeout:.1f}s")


class TaskFailedError(Exception):
    """Task execution failed error."""

    def __init__(self, task_id: str, status: str, errors: list | None = None):
        self.task_id = task_id
        self.status = status
        self.errors = errors or []
        super().__init__(
            f"Task {task_id} failed with status {status}"
            + (f": {errors}" if errors else "")
        )


class TaskPoller(Generic[T]):
    """Utility for polling task status with exponential backoff."""

    def __init__(
        self,
        check_fn: Callable[[str], T],
        task_id: str,
        timeout: int = 300,
        interval: int = 2,
        backoff_factor: float = 1.5,
        max_interval: int = 30,
    ):
        """
        Initialize task poller.

        Args:
            check_fn: Function to check task status (task_id) -> TaskDetails
            task_id: Task ID to monitor
            timeout: Maximum time to wait in seconds
            interval: Initial polling interval in seconds
            backoff_factor: Multiplier for exponential backoff
            max_interval: Maximum polling interval in seconds
        """
        self.check_fn = check_fn
        self.task_id = task_id
        self.timeout = timeout
        self.interval = interval
        self.backoff_factor = backoff_factor
        self.max_interval = max_interval

    def wait(
        self,
        on_progress: Callable[[T], None] | None = None,
    ) -> T:
        """
        Wait for task to complete with exponential backoff.

        Args:
            on_progress: Optional callback for progress updates

        Returns:
            Final task details

        Raises:
            TaskTimeoutError: If timeout exceeded
            TaskFailedError: If task failed
        """
        start_time = time.monotonic()
        current_interval = self.interval

        while True:
            elapsed = time.monotonic() - start_time

            if elapsed >= self.timeout:
                raise TaskTimeoutError(self.task_id, elapsed)

            # Check task status
            task = self.check_fn(self.task_id)

            # Call progress callback if provided
            if on_progress:
                on_progress(task)

            # Check if completed
            if task.is_completed:
                if task.is_successful:
                    return task
                else:
                    raise TaskFailedError(
                        self.task_id,
                        task.status.value,
                        task.errors if task.has_errors else None,
                    )

            # Sleep with exponential backoff
            sleep_time = min(current_interval, self.max_interval)
            remaining = self.timeout - elapsed
            sleep_time = min(sleep_time, remaining)

            if sleep_time > 0:
                time.sleep(sleep_time)

            current_interval *= self.backoff_factor


def wait_for_task(
    check_fn: Callable[[str], T],
    task_id: str,
    timeout: int = 300,
    interval: int = 2,
    on_progress: Callable[[T], None] | None = None,
) -> T:
    """
    Convenient function to wait for task completion.

    Args:
        check_fn: Function to check task status
        task_id: Task ID to monitor
        timeout: Maximum wait time in seconds
        interval: Initial polling interval in seconds
        on_progress: Optional progress callback

    Returns:
        Completed task details

    Raises:
        TaskTimeoutError: If timeout exceeded
        TaskFailedError: If task failed

    Example:
        >>> def check_status(task_id: str) -> TaskDetails:
        ...     return api.get_task_status(task_id)
        >>>
        >>> result = wait_for_task(check_status, "task-123", timeout=60)
        >>> print(f"Processed: {result.processed_items}")
    """
    poller = TaskPoller(
        check_fn=check_fn,
        task_id=task_id,
        timeout=timeout,
        interval=interval,
    )
    return poller.wait(on_progress=on_progress)
