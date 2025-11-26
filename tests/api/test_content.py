"""Tests for Content API."""

import pytest
from wb_api.api.content import ContentAPI


def test_content_api_has_methods():
    """Test that ContentAPI has all required methods."""
    methods = [
        "get_parent_categories",
        "get_subjects",
        "get_subject_characteristics",
        "get_cards",
        "iter_cards",
        "create_cards",
        "update_cards",
        "delete_cards",
        "recover_cards",
        "upload_media_by_url",
        "create_tag",
        "delete_tag",
    ]

    for method in methods:
        assert hasattr(ContentAPI, method)
