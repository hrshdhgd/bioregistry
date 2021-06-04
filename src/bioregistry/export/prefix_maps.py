# -*- coding: utf-8 -*-

"""Export the Bioregistry as a JSON-LD context."""

import json
import logging
from pathlib import Path
from typing import Mapping

import click

import bioregistry
from bioregistry.constants import DOCS_DATA
from bioregistry.schema import Collection

logger = logging.getLogger(__name__)


@click.command()
def generate_context_json_ld():
    """Generate various JSON-LD context files."""
    contexts_directory = Path(DOCS_DATA) / 'contexts'
    contexts_directory.mkdir(parents=True, exist_ok=True)

    with contexts_directory.joinpath('obo_context.jsonld').open('w') as file:
        json.dump(fp=file, indent=4, sort_keys=True, obj={
            "@context": get_obofoundry_prefix_map(),
        })

    for key, collection in bioregistry.read_collections().items():
        name = collection.context
        if name is None:
            continue
        with contexts_directory.joinpath(f'{name}_context').with_suffix('.jsonld').open('w') as file:
            json.dump(fp=file, indent=4, sort_keys=True, obj=get_collection_jsonld(key))


def get_collection_jsonld(identifier: str) -> Mapping[str, Mapping[str, str]]:
    """Get the JSON-LD context based on a given collection."""
    collection = bioregistry.get_collection(identifier)
    if collection is None:
        raise KeyError
    return collection.as_context_jsonld()


def collection_to_context_jsonlds(collection: Collection) -> str:
    """Get the JSON-LD context as a string from a given collection."""
    return json.dumps(collection.as_context_jsonld())


def get_obofoundry_prefix_map() -> Mapping[str, str]:
    """Get the OBO foundry prefix map."""
    rv = {}
    for prefix in bioregistry.read_registry():
        obofoundry_prefix = bioregistry.get_obofoundry_prefix(prefix)
        obofoundry_fmt = bioregistry.get_obofoundry_format(prefix)
        if obofoundry_prefix is None or obofoundry_fmt is None:
            continue
        rv[obofoundry_prefix] = obofoundry_fmt
    return rv


if __name__ == '__main__':
    generate_context_json_ld()