from utils import connect_to_database, find_node_url_by_id, WebSiteNotFoundError, ShortestPathNotFoundError


def find_shortest_path(start_url, end_url):
    """Find the shortest path between two nodes representing URLs in the database."""
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        MATCH (l1: Link {url: $start_url})-[edge_list: LINKS_TO * bfs..10]-(l2: Link {url: $end_url})
        RETURN edge_list LIMIT 1;
        """,
        {'start_url': start_url, 'end_url': end_url})

    row = cursor.fetchone()

    if row is None:
        cursor.execute("MATCH (l1: Link {url: $start_url}) RETURN l1;", {'start_url': start_url})
        row = cursor.fetchone()
        if row is None:
            raise WebSiteNotFoundError(start_url)
        cursor.execute("MATCH (l1: Link {url: $end_url}) RETURN l1;", {'end_url': end_url})
        row = cursor.fetchone()
        if row is None:
            raise WebSiteNotFoundError(end_url)
        raise ShortestPathNotFoundError(f'No path between {start_url} and {end_url}.')

    return row[0], cursor


def find_node_ids(relationships):
    """Return node IDs using the provided list of Relationship objects."""
    node_ids = [rel.start_id for rel in reversed(relationships)]
    node_ids.append(relationships[0].end_id)
    return node_ids


def iter_path_urls(node_ids, cursor):
    """Iterate path URLs using the provided node IDs."""
    for i, node_id in enumerate(node_ids):
        yield find_node_url_by_id(node_id, cursor)


def shortest_path(start_url, end_url):
    """Find the shortest path between two nodes representing URLs in the database, print their count and URLs."""
    relationships, cursor = find_shortest_path(start_url, end_url)
    node_ids = find_node_ids(relationships)
    print(f'Shortest path: {len(node_ids) - 1} clicks')
    for i, url in enumerate(iter_path_urls(node_ids, cursor)):
        print(f"{i} - {url}")




