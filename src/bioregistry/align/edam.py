# -*- coding: utf-8 -*-

"""Align EDAM with the Bioregistry."""

from typing import Mapping, Sequence

from bioregistry.align.utils import Aligner
from bioregistry.external.edam import get_edam

__all__ = [
    "EDAMAligner",
]


class EDAMAligner(Aligner):
    """Aligner for the EDAM ontology."""

    key = "edam"
    getter = get_edam
    alt_key_match = "name"
    curation_header = ("name", "description")

    def get_skip(self) -> Mapping[str, str]:
        """Get entries that should be skipped and their reasons."""
        return {
            "1164": "MIRIAM URI not relevant",
            "1175": "BioPAX ontologies aren't globally unique",
            "2582": "GO sub-hierarchy",
            "2583": "GO sub-hierarchy",
        }

    def get_curation_row(self, external_id, external_entry) -> Sequence[str]:
        """Prepare curation rows for unaligned EDAM ontology classes."""
        return [
            external_entry["name"],
            external_entry["description"],
        ]


if __name__ == "__main__":
    EDAMAligner.align()
