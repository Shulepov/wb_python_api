"""Tests for TokenDecoder."""

import pytest

from wb_api.auth import TokenDecoder


def test_token_decoder_invalid_token():
    """Test decoding invalid token."""
    with pytest.raises(ValueError):
        TokenDecoder.decode("invalid.token")


def test_token_decoder_is_expired():
    """Test checking if token is expired."""
    # Invalid token should be considered expired
    assert TokenDecoder.is_expired("invalid.token") is True


def test_token_decoder_has_category_access():
    """Test checking category access."""
    # Invalid token should not have access
    assert TokenDecoder.has_category_access("invalid.token", "content") is False


def test_token_decoder_validate_token():
    """Test token validation."""
    is_valid, error = TokenDecoder.validate_token("invalid.token")
    assert is_valid is False
    assert error is not None
