import requests
from requests.exceptions import ConnectionError
import functools

from bs4 import BeautifulSoup

from utils import connect_to_database, WebSiteNotFoundError


def save_to_database(start_url, urls):
    """Save nodes representing URLs and edges representing links to the database."""
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("MERGE (l:Link {url: $start_url});", {'start_url': start_url})

    for url in urls:
        cursor.execute("""
                        MERGE (l1: Link {url: $start_url})
                        MERGE (l2: Link {url: $url}) 
                        MERGE (l1)-[e:LINKS_TO]->(l2)
                        RETURN l1, e, l2;
                        """,
                       {'start_url': start_url, 'url': url})
    conn.commit()


def sanitize_url(url, domain_url=None):
    """Convert URL to the format http(s)://xxxxx.yy."""
    # memgraph.com/ -> memgraph.com
    if url[-1] == '/' and url.count('/') == 3:
        url = url[:-1]
    # memgraph.com + /docs
    if url[0] == '/' and domain_url is not None:

        url = domain_url + url
    # docs.memgraph.com/cypher-manu al/#clauses -> docs.memgraph.com/cypher-manual/
    div_id_pos = url.find('/#')
    if div_id_pos != -1:
        url = url[:div_id_pos + 1]

    position = url.find('www')
    if position != -1 and url[position - 3:position] == '://':
        url = url.replace('www.', '', 1)

    return url


def is_section_link(url):
    """Check if URL is a link to the section located at the same URL."""
    if url[0] == '#':
        return True
    return False


def sanitized_urls(urls, start_url):
    """Yield sanitized URLs from the provided list."""
    for url in urls:
        if url and not is_section_link(url):
            yield sanitize_url(url, start_url)


@functools.lru_cache(maxsize=None)
def scrap(start_url, depth=2):
    """Recursively find and store in database all website the links starting from start_url to the provided depth."""
    if depth == 0:
        return

    try:
        content = requests.get(start_url).content
    except ConnectionError:
        raise WebSiteNotFoundError(start_url)
    except Exception as e:
        # do not abort everything if getting content of one of the URLs fails for some reason
        print(e)
        return

    parser = 'html.parser'
    soup = BeautifulSoup(content, parser)

    clean_start_url = sanitize_url(start_url)
    link_elements = soup.find_all('a', href=True)
    urls = (link['href'] for link in link_elements if 'href' in link.attrs)
    clean_urls = [url for url in sanitized_urls(urls, clean_start_url)]

    save_to_database(clean_start_url, clean_urls)
    for url in clean_urls:
        if url != start_url:
            scrap(url, depth - 1)
