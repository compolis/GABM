"""Tests for generic seeded network utilities."""

import signal
import threading

import networkx as nx
import pytest

import gabm.abm.networks as networks
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


def test_homophily_favours_matching_feature_groups():
    graph = build_network(
        "homophily_weighted",
        list(range(20)),
        params={"scale": 20.0, "threshold": 10.0},
        seed=0,
        similarity_inputs=[["left", 0]] * 10 + [["right", 1]] * 10,
    )

    assert set(graph.edges) == (
        set(nx.complete_graph(range(10)).edges)
        | set(nx.complete_graph(range(10, 20)).edges)
    )


def test_homophily_default_weights_equal_explicit_uniform_weights():
    features = [["left", 0], ["right", 1], [None, 2], ["left", None]]
    default = build_network(
        "homophily_weighted", list(range(4)), seed=17,
        similarity_inputs=features,
    )
    explicit = build_network(
        "homophily_weighted", list(range(4)),
        params={"weights": [1.0, 1.0]}, seed=17,
        similarity_inputs=features,
    )

    assert set(default.edges) == set(explicit.edges)


def test_homophily_missing_values_do_not_count_as_matches():
    graph = build_network(
        "homophily_weighted", list(range(10)),
        params={"scale": 20.0, "threshold": 10.0}, seed=0,
        similarity_inputs=[[None, None]] * 10,
    )

    assert list(graph.nodes) == list(range(10))
    assert graph.number_of_edges() == 0


@pytest.mark.parametrize("disconnected", [False, True])
def test_diagnostics_metric_values_and_largest_component(disconnected):
    graph = nx.path_graph(4)
    if disconnected:
        graph.add_node("isolated")

    diagnostics = compute_diagnostics(graph, timeout_s=None)

    assert diagnostics["n_nodes"] == (5 if disconnected else 4)
    assert diagnostics["n_edges"] == 3
    assert diagnostics["density"] == pytest.approx(0.3 if disconnected else 0.5)
    assert diagnostics["mean_degree"] == pytest.approx(1.2 if disconnected else 1.5)
    assert diagnostics["median_degree"] == (1 if disconnected else 1.5)
    assert diagnostics["max_degree"] == 2
    assert sum(diagnostics["degree_histogram"]["counts"]) == len(graph)
    assert diagnostics["n_connected_components"] == (2 if disconnected else 1)
    assert diagnostics["largest_component_size"] == 4
    assert diagnostics["average_clustering"] == 0
    assert diagnostics["diameter"] == 3
    assert diagnostics["average_shortest_path_length"] == pytest.approx(5 / 3)
    assert not diagnostics["timed_out"]
    if disconnected:
        assert "4/5 nodes" in diagnostics["diameter_note"]
        assert "4/5 nodes" in diagnostics["average_shortest_path_length_note"]


@pytest.mark.parametrize("timeout_s", [None, 0, -1])
def test_diagnostics_disabled_timeout_does_not_arm_timer(monkeypatch, timeout_s):
    def unexpected_timer(*args):
        pytest.fail("A disabled timeout must not arm a timer")

    monkeypatch.setattr(signal, "setitimer", unexpected_timer, raising=False)

    assert not compute_diagnostics(nx.path_graph(4), timeout_s=timeout_s)["timed_out"]


@pytest.mark.skipif(
    not hasattr(signal, "setitimer")
    or not hasattr(signal, "SIGALRM")
    or threading.current_thread() is not threading.main_thread(),
    reason="POSIX diagnostics timeout requires the main thread",
)
def test_diagnostics_timeout_returns_partial_results_and_restores_handler(
    monkeypatch, caplog,
):
    original_handler = signal.getsignal(signal.SIGALRM)

    def interrupt_clustering(graph):
        signal.raise_signal(signal.SIGALRM)
        pytest.fail("The installed alarm handler must interrupt diagnostics")

    monkeypatch.setattr(nx, "average_clustering", interrupt_clustering)
    diagnostics = compute_diagnostics(nx.path_graph(4), timeout_s=30)

    assert diagnostics["timed_out"]
    assert diagnostics["timeout_s"] == 30
    assert diagnostics["n_nodes"] == 4
    assert "average_clustering" not in diagnostics
    assert "diameter" not in diagnostics
    assert "elapsed_s" in diagnostics
    assert "partial results saved" in caplog.text
    assert signal.getsignal(signal.SIGALRM) == original_handler
    assert signal.getitimer(signal.ITIMER_REAL)[0] == 0


@pytest.mark.parametrize("n_nodes", [3, 4])
def test_diagnostics_size_caps_include_boundary(monkeypatch, n_nodes):
    monkeypatch.setattr(networks, "_CLUSTERING_NODE_CAP", 3)
    monkeypatch.setattr(networks, "_PATHLEN_NODE_CAP", 3)
    monkeypatch.setattr(networks, "_DIAMETER_NODE_CAP", 3)

    diagnostics = compute_diagnostics(nx.path_graph(n_nodes), timeout_s=None)

    for metric in ("average_clustering", "average_shortest_path_length", "diameter"):
        if n_nodes == 3:
            assert metric in diagnostics
            assert f"{metric}_skipped_reason" not in diagnostics
        else:
            assert metric not in diagnostics
            assert diagnostics[f"{metric}_skipped_reason"] == "n=4 exceeds cap 3"


def test_connect_components_preserves_exact_seeded_bridges():
    graph = nx.Graph([(0, 1), (2, 3), (4, 5), (6, 7)])

    assert connect_components(graph, seed=123) == 3
    assert {tuple(sorted(edge)) for edge in graph.edges} == {
        (0, 1), (0, 3), (1, 4), (1, 6), (2, 3), (4, 5), (6, 7),
    }
