"""Tests for task utilities."""

import time

import pytest

from wb_api.models.base import BaseTaskDetails, TaskStatus
from wb_api.utils.tasks import TaskFailedError, TaskPoller, TaskTimeoutError, wait_for_task


class MockTaskDetails(BaseTaskDetails):
    """Mock task details for testing."""

    pass


def test_task_poller_success():
    """Test task poller with successful completion."""
    call_count = 0

    def check_fn(task_id: str) -> MockTaskDetails:
        nonlocal call_count
        call_count += 1

        if call_count < 3:
            return MockTaskDetails(
                task_id=task_id,
                status=TaskStatus.PROCESSING,
                total_items=100,
                processed_items=call_count * 30,
            )
        return MockTaskDetails(
            task_id=task_id,
            status=TaskStatus.COMPLETED,
            total_items=100,
            processed_items=100,
        )

    poller = TaskPoller(
        check_fn=check_fn,
        task_id="test-task",
        timeout=10,
        interval=0.1,
    )

    result = poller.wait()

    assert result.is_completed
    assert result.is_successful
    assert result.processed_items == 100
    assert call_count >= 3


def test_task_poller_with_progress_callback():
    """Test task poller with progress callback."""
    progress_updates = []

    def check_fn(task_id: str) -> MockTaskDetails:
        if len(progress_updates) < 2:
            return MockTaskDetails(
                task_id=task_id,
                status=TaskStatus.PROCESSING,
                total_items=100,
                processed_items=len(progress_updates) * 50,
            )
        return MockTaskDetails(
            task_id=task_id,
            status=TaskStatus.COMPLETED,
            total_items=100,
            processed_items=100,
        )

    def on_progress(task: MockTaskDetails):
        progress_updates.append(task.progress_percent)

    poller = TaskPoller(
        check_fn=check_fn,
        task_id="test-task",
        timeout=10,
        interval=0.1,
    )

    result = poller.wait(on_progress=on_progress)

    assert result.is_completed
    assert len(progress_updates) >= 3
    assert progress_updates[-1] == 100.0


def test_task_poller_timeout():
    """Test task poller timeout."""

    def check_fn(task_id: str) -> MockTaskDetails:
        return MockTaskDetails(
            task_id=task_id,
            status=TaskStatus.PROCESSING,
            total_items=100,
            processed_items=50,
        )

    poller = TaskPoller(
        check_fn=check_fn,
        task_id="test-task",
        timeout=1,
        interval=0.2,
    )

    with pytest.raises(TaskTimeoutError) as exc_info:
        poller.wait()

    assert exc_info.value.task_id == "test-task"
    assert exc_info.value.timeout >= 1.0


def test_task_poller_failed():
    """Test task poller with failed task."""

    def check_fn(task_id: str) -> MockTaskDetails:
        return MockTaskDetails(
            task_id=task_id,
            status=TaskStatus.ERROR,
            total_items=100,
            processed_items=50,
            errors_count=5,
            errors=[{"error": "Something went wrong"}],
        )

    poller = TaskPoller(
        check_fn=check_fn,
        task_id="test-task",
        timeout=10,
        interval=0.1,
    )

    with pytest.raises(TaskFailedError) as exc_info:
        poller.wait()

    assert exc_info.value.task_id == "test-task"
    assert exc_info.value.status == "error"


def test_wait_for_task_convenience_function():
    """Test wait_for_task convenience function."""
    call_count = 0

    def check_fn(task_id: str) -> MockTaskDetails:
        nonlocal call_count
        call_count += 1

        if call_count < 2:
            return MockTaskDetails(
                task_id=task_id,
                status=TaskStatus.PROCESSING,
                total_items=100,
                processed_items=50,
            )
        return MockTaskDetails(
            task_id=task_id,
            status=TaskStatus.COMPLETED,
            total_items=100,
            processed_items=100,
        )

    result = wait_for_task(
        check_fn=check_fn,
        task_id="test-task",
        timeout=10,
        interval=0.1,
    )

    assert result.is_completed
    assert result.is_successful


def test_task_details_properties():
    """Test BaseTaskDetails properties."""
    # Test completed task
    task = MockTaskDetails(
        task_id="test",
        status=TaskStatus.COMPLETED,
        total_items=100,
        processed_items=100,
    )
    assert task.is_completed
    assert task.is_successful
    assert not task.has_errors
    assert task.progress_percent == 100.0

    # Test task with errors
    task = MockTaskDetails(
        task_id="test",
        status=TaskStatus.ERROR,
        total_items=100,
        processed_items=50,
        errors_count=5,
        errors=[{"error": "test"}],
    )
    assert task.is_completed
    assert not task.is_successful
    assert task.has_errors
    assert task.progress_percent == 50.0

    # Test pending task
    task = MockTaskDetails(
        task_id="test",
        status=TaskStatus.PENDING,
        total_items=0,
        processed_items=0,
    )
    assert not task.is_completed
    assert not task.is_successful
    assert task.progress_percent == 0.0
