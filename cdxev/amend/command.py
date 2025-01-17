import logging

from cdxev.auxiliary.sbomFunctions import walk_components

from .operations import Operation

__operations: list[Operation] = []
logger = logging.getLogger(__name__)


def register_operation(operation: Operation) -> None:
    """
    Registers an operation for the amend command.

    This function is typically invoked in __init__.py.
    """
    __operations.append(operation)


def run(sbom: dict) -> None:
    """
    Runs the amend command on an SBOM. The SBOM is modified in-place.

    :param dict sbom: The SBOM model.
    """
    _prepare(sbom)
    _metadata(sbom)
    walk_components(sbom, _do_amend, skip_meta=True)


def _prepare(sbom: dict) -> None:
    for operation in __operations:
        operation.prepare(sbom)


def _metadata(sbom: dict) -> None:
    if "metadata" not in sbom:
        return

    logger.debug("Processing metadata")
    metadata = sbom["metadata"]
    for operation in __operations:
        operation.handle_metadata(metadata)


def _do_amend(component: dict) -> None:
    for operation in __operations:
        logger.debug(
            "Processing component %s", (component.get("bom-ref", "<no bom-ref>"))
        )
        operation.handle_component(component)
