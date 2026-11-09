"""Generic seeded network construction, diagnostics, and connectivity repair."""
from __future__ import annotations

__version__ = "0.3.0"
__author__ = ["GABM contributors"]
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import logging
import math
import signal
import threading
import time
from contextlib import contextmanager
from typing import Any, Hashable, Iterable, Mapping, Sequence

import networkx as nx
import numpy as np


NETWORK_TYPES = (
    "stochastic_block",
    "erdos_renyi",
    "watts_strogatz",
    "barabasi_albert",
    "homophily_weighted",
)
__all__ = [
    "NETWORK_TYPES",
    "build_network",
    "compute_diagnostics",
    "connect_components",
]

_CLUSTERING_NODE_CAP = 5000
_PATHLEN_NODE_CAP = 2000
_DIAMETER_NODE_CAP = 2000
_PATHLEN_SAMPLE_CAP = 500


def build_network(
    network_type: str,
    node_ids: Sequence[Hashable],
    params: Mapping[str, Any] | None = None,
    seed: int = 42,
    *,
    block_membership: Sequence[Hashable] | None = None,
    block_order: Sequence[Hashable] | None = None,
    similarity_inputs: Sequence[Sequence[Any]] | None = None,
) -> nx.Graph:
    """Build a seeded undirected graph over caller-supplied node IDs.

    ``block_membership`` supplies one block label per node for the
    stochastic-block builder. Nodes are grouped in first-seen block order
    unless ``block_order`` supplies an explicit order, including empty blocks.
    ``similarity_inputs`` supplies one row of categorical or numeric features
    per node for the homophily-weighted builder; the caller owns feature
    selection and interpretation.
    """
    if network_type not in NETWORK_TYPES:
        raise ValueError(
            f"Unknown network_type {network_type!r}; "
            f"valid options: {NETWORK_TYPES}"
        )

    nodes = list(node_ids)
    if not nodes:
        raise ValueError("Cannot build a network with zero nodes.")
    builder_params = dict(params or {})

    if network_type == "stochastic_block":
        return _build_stochastic_block(
            nodes, builder_params, int(seed), block_membership, block_order
        )
    if network_type == "erdos_renyi":
        return _build_erdos_renyi(nodes, builder_params, int(seed))
    if network_type == "watts_strogatz":
        return _build_watts_strogatz(nodes, builder_params, int(seed))
    if network_type == "barabasi_albert":
        return _build_barabasi_albert(nodes, builder_params, int(seed))
    return _build_homophily_weighted(
        nodes, builder_params, int(seed), similarity_inputs
    )


def _build_stochastic_block(
    nodes: Sequence[Hashable],
    params: Mapping[str, Any],
    seed: int,
    block_membership: Sequence[Hashable] | None,
    block_order: Sequence[Hashable] | None,
) -> nx.Graph:
    p_intra = float(params.get("p_intra", 0.15))
    p_inter = float(params.get("p_inter", 0.05))
    membership = (
        list(block_membership)
        if block_membership is not None else [0] * len(nodes)
    )
    if len(membership) != len(nodes):
        raise ValueError("stochastic_block: block_membership must match node_ids.")

    block_labels = (
        list(dict.fromkeys(membership))
        if block_order is None else list(block_order)
    )
    if len(block_labels) != len(set(block_labels)):
        raise ValueError("stochastic_block: block_order labels must be unique.")
    if any(label not in block_labels for label in membership):
        raise ValueError(
            "stochastic_block: block_order must include every membership label."
        )
    blocks = {label: [] for label in block_labels}
    for node, label in zip(nodes, membership):
        blocks[label].append(node)

    ordered_nodes = [node for label in block_labels for node in blocks[label]]
    sizes = [len(blocks[label]) for label in block_labels]
    p_matrix = [
        [p_intra if i == j else p_inter for j in range(len(sizes))]
        for i in range(len(sizes))
    ]
    graph = nx.stochastic_block_model(sizes, p_matrix, seed=seed)
    return _relabel_to_node_ids(graph, ordered_nodes)


def _build_erdos_renyi(
    nodes: Sequence[Hashable], params: Mapping[str, Any], seed: int
) -> nx.Graph:
    p = float(params.get("p", 0.10))
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"erdos_renyi: p must be in [0, 1], got {p!r}.")
    graph = nx.erdos_renyi_graph(len(nodes), p, seed=seed)
    return _relabel_to_node_ids(graph, nodes)


def _build_watts_strogatz(
    nodes: Sequence[Hashable], params: Mapping[str, Any], seed: int
) -> nx.Graph:
    n = len(nodes)
    k = int(params.get("k", 6))
    beta = float(params.get("beta", 0.1))
    if k < 2 or k % 2 != 0:
        raise ValueError(
            f"watts_strogatz: k must be an even integer >= 2, got {k!r}."
        )
    if k >= n:
        raise ValueError(f"watts_strogatz: k ({k}) must be < n ({n}).")
    if not 0.0 <= beta <= 1.0:
        raise ValueError(f"watts_strogatz: beta must be in [0, 1], got {beta!r}.")
    graph = nx.watts_strogatz_graph(n, k, beta, seed=seed)
    return _relabel_to_node_ids(graph, nodes)


def _build_barabasi_albert(
    nodes: Sequence[Hashable], params: Mapping[str, Any], seed: int
) -> nx.Graph:
    n = len(nodes)
    m = int(params.get("m", 3))
    if m < 1 or m >= n:
        raise ValueError(
            f"barabasi_albert: m must satisfy 1 <= m < n, got m={m}, n={n}."
        )
    graph = nx.barabasi_albert_graph(n, m, seed=seed)
    return _relabel_to_node_ids(graph, nodes)


def _build_homophily_weighted(
    nodes: Sequence[Hashable],
    params: Mapping[str, Any],
    seed: int,
    similarity_inputs: Sequence[Sequence[Any]] | None,
) -> nx.Graph:
    if similarity_inputs is None:
        raise ValueError(
            "homophily_weighted: similarity_inputs are required."
        )
    rows = [list(row) for row in similarity_inputs]
    if len(rows) != len(nodes):
        raise ValueError(
            "homophily_weighted: similarity_inputs must match node_ids."
        )
    n_features = len(rows[0])
    if n_features == 0 or any(len(row) != n_features for row in rows):
        raise ValueError(
            "homophily_weighted: each node must have the same non-empty "
            "similarity_inputs row."
        )

    weights = params.get("weights")
    scale = float(params.get("scale", 6.0))
    threshold = float(params.get("threshold", 3.0))
    if weights is None:
        weights = [1.0] * n_features
    weights = [float(weight) for weight in weights]
    if len(weights) != n_features:
        raise ValueError(
            "homophily_weighted: len(weights) must equal the feature count."
        )
    weight_sum = sum(weights)
    if weight_sum <= 0:
        raise ValueError(
            "homophily_weighted: weights must sum to a positive value."
        )
    weights = [weight / weight_sum for weight in weights]

    columns = [[row[index] for row in rows] for index in range(n_features)]
    is_numeric = []
    ranges = []
    for column in columns:
        numeric = all(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            for value in column if value is not None
        )
        is_numeric.append(numeric)
        if numeric:
            values = [value for value in column if value is not None]
            value_range = (max(values) - min(values)) if values else 0.0
            ranges.append(float(value_range) if value_range > 0 else 1.0)
        else:
            ranges.append(1.0)

    rng = np.random.default_rng(seed)
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            similarity = 0.0
            for k, column in enumerate(columns):
                left, right = column[i], column[j]
                if left is None or right is None:
                    value_similarity = 0.0
                elif is_numeric[k]:
                    value_similarity = (
                        1.0 - abs(float(left) - float(right)) / ranges[k]
                    )
                else:
                    value_similarity = 1.0 if left == right else 0.0
                similarity += weights[k] * value_similarity
            probability = 1.0 / (
                1.0 + math.exp(-(scale * similarity - threshold))
            )
            if rng.random() < probability:
                graph.add_edge(nodes[i], nodes[j])
    return graph


def _relabel_to_node_ids(
    graph: nx.Graph, ordered_nodes: Sequence[Hashable]
) -> nx.Graph:
    return nx.relabel_nodes(
        graph, {index: node_id for index, node_id in enumerate(ordered_nodes)}
    )


def compute_diagnostics(
    graph: nx.Graph,
    node_attributes: Mapping[str, Mapping[Hashable, Any]] | None = None,
    timeout_s: float | None = 30.0,
) -> dict[str, Any]:
    """Compute cheap and capped structural metrics for a graph.

    Each mapping in ``node_attributes`` associates node IDs with categorical
    values. Its assortativity is returned under ``assortativity_<name>``.
    """
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    degrees = [degree for _, degree in graph.degree()]
    max_possible_edges = n * (n - 1) / 2 if n > 1 else 0

    out: dict[str, Any] = {
        "n_nodes": n,
        "n_edges": m,
        "density": (m / max_possible_edges) if max_possible_edges else 0.0,
        "mean_degree": float(np.mean(degrees)) if degrees else 0.0,
        "median_degree": float(np.median(degrees)) if degrees else 0.0,
        "max_degree": int(max(degrees)) if degrees else 0,
        "degree_histogram": _degree_histogram(degrees, bins=20),
        "n_connected_components": nx.number_connected_components(graph),
        "largest_component_size": (
            max(len(component) for component in nx.connected_components(graph))
            if n > 0 else 0
        ),
    }

    for name, values in (node_attributes or {}).items():
        value_map = {
            node_id: value for node_id, value in values.items()
            if value is not None and node_id in graph
        }
        key = f"assortativity_{name}"
        if not value_map or len(value_map) != n:
            out[key] = None
            continue
        graph_attribute = f"_gabm_diagnostic_{name}"
        try:
            nx.set_node_attributes(graph, value_map, graph_attribute)
            out[key] = float(
                nx.attribute_assortativity_coefficient(graph, graph_attribute)
            )
        except Exception as error:  # diagnostics must not abort a simulation
            out[key] = None
            out[f"{key}_error"] = str(error)
        finally:
            for node_id in list(graph.nodes):
                graph.nodes[node_id].pop(graph_attribute, None)

    out["timed_out"] = False
    started = time.monotonic()
    try:
        with _wallclock_timeout(timeout_s):
            if n > _CLUSTERING_NODE_CAP:
                out["average_clustering_skipped_reason"] = (
                    f"n={n} exceeds cap {_CLUSTERING_NODE_CAP}"
                )
            else:
                out["average_clustering"] = float(nx.average_clustering(graph))

            if n > _PATHLEN_NODE_CAP:
                out["average_shortest_path_length_skipped_reason"] = (
                    f"n={n} exceeds cap {_PATHLEN_NODE_CAP}"
                )
                out["diameter_skipped_reason"] = (
                    f"n={n} exceeds cap {_DIAMETER_NODE_CAP}"
                )
            else:
                if nx.is_connected(graph):
                    target = graph
                    sub_note = None
                else:
                    largest_component = max(
                        nx.connected_components(graph), key=len
                    )
                    target = graph.subgraph(largest_component).copy()
                    sub_note = (
                        f"graph disconnected; computed on largest component "
                        f"({target.number_of_nodes()}/{n} nodes)"
                    )

                if target.number_of_nodes() <= _DIAMETER_NODE_CAP:
                    out["diameter"] = int(nx.diameter(target))
                    if sub_note:
                        out["diameter_note"] = sub_note
                else:
                    out["diameter_skipped_reason"] = (
                        f"largest-component n={target.number_of_nodes()} "
                        f"exceeds cap {_DIAMETER_NODE_CAP}"
                    )

                if target.number_of_nodes() <= _PATHLEN_SAMPLE_CAP:
                    out["average_shortest_path_length"] = float(
                        nx.average_shortest_path_length(target)
                    )
                else:
                    out["average_shortest_path_length"] = (
                        _sampled_average_path_length(
                            target, sample=_PATHLEN_SAMPLE_CAP, seed=0
                        )
                    )
                    out["average_shortest_path_length_note"] = (
                        f"estimated from {_PATHLEN_SAMPLE_CAP} sampled sources"
                    )
                if sub_note and "average_shortest_path_length" in out:
                    out["average_shortest_path_length_note"] = (
                        sub_note + "; " + out.get(
                            "average_shortest_path_length_note", ""
                        )
                    ).rstrip("; ")
    except _DiagnosticsTimeout:
        out["timed_out"] = True
        out["timeout_s"] = float(timeout_s) if timeout_s else None
        logging.warning(
            "Network diagnostics timed out after %.1fs; partial results saved.",
            timeout_s,
        )

    out["elapsed_s"] = round(time.monotonic() - started, 4)
    return out


def connect_components(graph: nx.Graph, seed: int = 42) -> int:
    """Connect graph components using one seeded edge per smaller component.

    Returns the number of edges added. Comparable node IDs retain their
    natural ordering; mixed incomparable types use a stable type-and-repr order.
    """
    if not isinstance(graph, nx.Graph) or graph.number_of_nodes() == 0:
        return 0
    if nx.is_connected(graph):
        return 0

    components = [
        _stable_sorted(component)
        for component in nx.connected_components(graph)
    ]
    try:
        components.sort(key=lambda component: (-len(component), component[0]))
    except TypeError:
        components.sort(
            key=lambda component: (
                -len(component),
                _stable_node_key(component[0]),
            )
        )
    largest = components[0]
    rng = np.random.default_rng(seed)
    for component in components[1:]:
        left = largest[int(rng.integers(0, len(largest)))]
        right = component[int(rng.integers(0, len(component)))]
        graph.add_edge(left, right)
    return len(components) - 1


def _stable_sorted(values: Iterable[Hashable]) -> list[Hashable]:
    try:
        return sorted(values)
    except TypeError:
        return sorted(values, key=_stable_node_key)


def _stable_node_key(value: Hashable) -> tuple[str, str, str]:
    value_type = type(value)
    return value_type.__module__, value_type.__qualname__, repr(value)


def _degree_histogram(
    degrees: Sequence[int], bins: int = 20
) -> dict[str, list[float] | list[int]]:
    if not degrees:
        return {"bin_edges": [], "counts": []}
    counts, edges = np.histogram(degrees, bins=bins)
    return {
        "bin_edges": [float(edge) for edge in edges],
        "counts": [int(count) for count in counts],
    }


def _sampled_average_path_length(
    graph: nx.Graph, sample: int, seed: int
) -> float:
    rng = np.random.default_rng(seed)
    nodes = list(graph.nodes)
    chosen = rng.choice(len(nodes), size=min(sample, len(nodes)), replace=False)
    total = 0.0
    pairs = 0
    for index in chosen:
        source = nodes[int(index)]
        lengths = nx.single_source_shortest_path_length(graph, source)
        for target, distance in lengths.items():
            if target == source:
                continue
            total += distance
            pairs += 1
    return total / pairs if pairs else 0.0


class _DiagnosticsTimeout(Exception):
    pass


@contextmanager
def _wallclock_timeout(seconds: float | None):
    """Apply a POSIX wall-clock timeout when running on the main thread."""
    if (
        seconds is None
        or seconds <= 0
        or not hasattr(signal, "SIGALRM")
        or threading.current_thread() is not threading.main_thread()
    ):
        yield
        return

    def timeout_handler(signum, frame):
        raise _DiagnosticsTimeout()

    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, float(seconds))
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
