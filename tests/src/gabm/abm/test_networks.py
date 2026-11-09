"""Tests for generic seeded network utilities."""

import networkx as nx
import pytest

from gabm.abm.networks import (
    NETWORK_TYPES,
    build_network,
    compute_diagnostics,
    connect_components,
)


def _build_all(node_ids):
    features = [
        (index % 2, float(index), "left" if index % 2 else "right")
        for index in range(len(node_ids))
    ]
    params = {
        "stochastic_block": {"p_intra": 0.6, "p_inter": 0.1},
        "erdos_renyi": {"p": 0.2},
        "watts_strogatz": {"k": 4, "beta": 0.2},
        "barabasi_albert": {"m": 2},
        "homophily_weighted": {"weights": [1.0, 1.0, 1.0]},
    }
    return {
        network_type: build_network(
            network_type,
            node_ids,
            params=params[network_type],
            seed=17,
            block_membership=[index % 2 for index in range(len(node_ids))],
            similarity_inputs=features,
        )
        for network_type in NETWORK_TYPES
    }


def test_builders_use_caller_node_ids_and_repeat_for_seed():
    node_ids = [f"person-{index}" for index in range(20)]

    first = _build_all(node_ids)
    second = _build_all(node_ids)

    for network_type in NETWORK_TYPES:
        assert isinstance(first[network_type], nx.Graph)
        assert set(first[network_type].nodes) == set(node_ids)
        assert set(first[network_type].edges) == set(second[network_type].edges)


def test_stochastic_block_groups_nodes_in_first_seen_label_order():
    node_ids = [10, 20, 30, 40]
    membership = ["second", "first", "second", "first"]

    graph = build_network(
        "stochastic_block",
        node_ids,
        params={"p_intra": 0.8, "p_inter": 0.1},
        seed=7,
        block_membership=membership,
    )
    expected = nx.stochastic_block_model(
        [2, 2], [[0.8, 0.1], [0.1, 0.8]], seed=7
    )
    expected = nx.relabel_nodes(
        expected, {0: 10, 1: 30, 2: 20, 3: 40}
    )

    assert set(graph.edges) == set(expected.edges)


def test_stochastic_block_preserves_explicit_empty_blocks():
    node_ids = [10, 20, 30, 40]
    membership = [1, 1, 1, 1]

    graph = build_network(
        "stochastic_block",
        node_ids,
        params={"p_intra": 0.8, "p_inter": 0.1},
        seed=7,
        block_membership=membership,
        block_order=(0, 1),
    )
    expected = nx.stochastic_block_model(
        [0, 4], [[0.8, 0.1], [0.1, 0.8]], seed=7
    )
    expected = nx.relabel_nodes(
        expected, {0: 10, 1: 20, 2: 30, 3: 40}
    )

    assert set(graph.edges) == set(expected.edges)


@pytest.mark.parametrize(
    ("network_type", "params"),
    [
        ("not-a-network", {}),
        ("erdos_renyi", {"p": 1.1}),
        ("watts_strogatz", {"k": 3}),
        ("barabasi_albert", {"m": 0}),
    ],
)
def test_invalid_builder_inputs_raise(network_type, params):
    with pytest.raises(ValueError):
        build_network(network_type, list(range(10)), params=params)


def test_build_network_rejects_empty_nodes_and_invalid_inputs():
    with pytest.raises(ValueError, match="zero nodes"):
        build_network("erdos_renyi", [])

    with pytest.raises(ValueError, match="block_membership"):
        build_network(
            "stochastic_block",
            [1, 2],
            block_membership=[0],
        )

    with pytest.raises(ValueError, match="similarity_inputs are required"):
        build_network("homophily_weighted", [1, 2])

    with pytest.raises(ValueError, match="feature count"):
        build_network(
            "homophily_weighted",
            [1, 2],
            params={"weights": [1.0, 2.0]},
            similarity_inputs=[["a"], ["b"]],
        )


def test_diagnostics_support_caller_defined_node_attributes():
    graph = nx.path_graph(4)
    node_attributes = {"side": {0: "A", 1: "A", 2: "B", 3: "B"}}

    diagnostics = compute_diagnostics(
        graph, node_attributes=node_attributes, timeout_s=10
    )

    assert diagnostics["n_nodes"] == 4
    assert diagnostics["n_edges"] == 3
    assert diagnostics["assortativity_side"] == pytest.approx(1 / 3)
    assert all(
        "_gabm_diagnostic_side" not in graph.nodes[node]
        for node in graph.nodes
    )


def test_connect_components_is_seeded_and_leaves_connected_graphs_alone():
    def disconnected_graph():
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (2, 3), (4, 5)])
        return graph

    first = disconnected_graph()
    second = disconnected_graph()

    assert connect_components(first, seed=23) == 2
    assert connect_components(second, seed=23) == 2
    assert nx.is_connected(first)
    assert set(first.edges) == set(second.edges)
    assert connect_components(first, seed=23) == 0
    assert connect_components(nx.Graph(), seed=23) == 0


def test_connect_components_supports_mixed_node_id_types():
    graph = nx.Graph()
    graph.add_edges_from([(1, "one"), (2.0, "two")])

    assert connect_components(graph, seed=23) == 1
    assert nx.is_connected(graph)
