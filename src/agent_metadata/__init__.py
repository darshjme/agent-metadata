"""agent-metadata: metadata tagging and annotation for agent outputs."""

from .metadata import Metadata
from .annotated import Annotated
from .store import MetadataStore
from .decorator import annotate

__all__ = ["Metadata", "Annotated", "MetadataStore", "annotate"]
__version__ = "0.1.0"
