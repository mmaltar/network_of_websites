import mgclient
from settings import DATABASE_HOST, DATABASE_PORT


class WebSiteNotFoundError(Exception):
    pass


class ShortestPathNotFoundError(Exception):
    pass


def connect_to_database():
    return mgclient.connect(host=DATABASE_HOST, port=DATABASE_PORT)


def find_node_url_by_id(node_id, cursor):
    cursor.execute(
        """
        MATCH (n) 
        WHERE id(n) = $id
        RETURN n.url;
        """,
        {'id': node_id})
    row = cursor.fetchone()
    return row[0]