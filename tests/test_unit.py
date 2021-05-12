import pytest

from network import sanitize_url, save_to_database
from utils import connect_to_database


def test_sanitize_url():
    url = sanitize_url('https://google.com/')
    assert url == 'https://google.com'
    url = sanitize_url('https://www.google.com/')
    assert url == 'https://google.com'
    url = sanitize_url('https://memgraph.com/content/')
    assert url == 'https://memgraph.com/content/'
    url = sanitize_url('docs.memgraph.com/cypher-manual/#clauses')
    assert url == 'docs.memgraph.com/cypher-manual/'
    url = sanitize_url('/docs', sanitize_url('https://memgraph.com/'))
    assert url == 'https://memgraph.com/docs'


def test_save_to_database():
    start_url = 'https://example.com'
    urls = ['https://example.com/example1', 'https://example.com/example2', 'https://example2.com/example/']
    save_to_database(start_url, urls)

    conn = connect_to_database()
    cursor = conn.cursor()

    for url in urls:
        cursor.execute("""
                           MATCH (l1: Link {url: $start_url})
                           MATCH (l2: Link {url: $url}) 
                           MATCH (l1)-[e:LINKS_TO]->(l2)
                           RETURN l1, e, l2;
                           """,
                       {'start_url': start_url, 'url': url})
        row = cursor.fetchone()
        assert row is not None
        assert any(el.properties.get('url', None) == url for el in row)
