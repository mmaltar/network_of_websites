import pytest

from network import scrap
from path import find_shortest_path, find_node_ids, iter_path_urls
from utils import connect_to_database


def scrap_and_populate_db(url):
    scrap(url)
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        MATCH (l: Link {url: $url})
        RETURN l;
        """,
        {'url': url})

    return cursor


def test_network():
    url = 'https://memgraph.com'

    cursor = scrap_and_populate_db(url)
    row = cursor.fetchone()
    assert row[0] is not None


def test_path():
    start_url = 'https://memgraph.com'
    end_url = 'https://discourse.memgraph.com/t/memgraph-lab-1-1-0-is-now-available/26'
    scrap_and_populate_db(start_url)
    relationships, cursor = find_shortest_path(start_url, end_url)
    node_ids = find_node_ids(relationships)
    path_urls = list(iter_path_urls(node_ids, cursor))
    assert len(path_urls) == 3
    assert 'https://discourse.memgraph.com' in path_urls

