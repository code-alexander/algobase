"""Unit tests for the ARC-19 Pydantic model."""

import pytest
from pydantic import ValidationError

from algobase.choices import Arc
from algobase.models.arc3 import Arc3Metadata
from algobase.models.arc19 import Arc19Metadata
from tests.types import FixtureDict


def test_no_arc3_metadata() -> None:
    """Test that validation succeeds when no ARC-3 metadata is present."""
    metadata = Arc19Metadata()
    assert isinstance(metadata, Arc19Metadata)
    assert metadata.arc == Arc.ARC19
    assert metadata.arc3_metadata is None


def test_arc3_metadata_valid(arc3_metadata_fixture: FixtureDict) -> None:
    """Test that validation succeeds when ARC-3 metadata is compliant with ARC-19."""
    test_dict = arc3_metadata_fixture.copy()
    test_dict.pop("extra_metadata")
    arc3_metadata = Arc3Metadata.model_validate(test_dict)
    metadata = Arc19Metadata(arc3_metadata=arc3_metadata)
    assert isinstance(metadata, Arc19Metadata)
    assert metadata.arc == Arc.ARC19
    assert isinstance(metadata.arc3_metadata, Arc3Metadata)
    assert metadata.arc3_metadata.arc == Arc.ARC3


def test_arc3_metadata_invalid(arc3_metadata_fixture: FixtureDict) -> None:
    """Test that validation fails when ARC-3 metadata is not compliant with ARC-19."""
    arc3_metadata = Arc3Metadata.model_validate(arc3_metadata_fixture)
    with pytest.raises(ValidationError):
        Arc19Metadata(arc3_metadata=arc3_metadata)
