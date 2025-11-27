"""Pydantic validation models for PhotoCluster."""

from pydantic import BaseModel, Field
from pydantic.types import DirectoryPath


class PhotoclusterInputs(BaseModel):
    """Pydantic model for validating photocluster function inputs."""

    input_dir: DirectoryPath = Field(
        ..., description="Directory containing images to cluster"
    )
    sensitivity: float = Field(
        ...,
        description="Clustering sensitivity as proportion (0.0-1.0). Lower values = stricter clustering.",
        ge=0.0,
        le=1.0,
    )
