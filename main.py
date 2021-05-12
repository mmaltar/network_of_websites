import argparse

from path import shortest_path
from network import scrap, sanitize_url


def verified_url_format(url):
    if url != sanitize_url(url):
        raise argparse.ArgumentTypeError(f'URL {url} is not in valid format.')
    return url


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="""Use 'network' to scrap the network for website links or 'path' to find 
                                            the shortest path to the given website.""", dest='job')

    parser_network = subparsers.add_parser('network')
    parser_network.add_argument("START_URL", help='Starting URL.')
    parser_network.add_argument('-d', '--depth', help='Scraping depth.', type=int, default=2)

    parser_path = subparsers.add_parser('path')
    parser_path.add_argument("START_URL", type=verified_url_format,
                             help="""
                                    Starting URL in format 'https://xxxxx.yy', 'https://xxxx.yy/zzz/' or 
                                    'https://xxxx.yy/zzz')
                                  """)

    parser_path.add_argument("END_URL", type=verified_url_format,
                             help="""
                                    Path end URL in format 'https://xxxxx.yy', 'https://xxxx.yy/zzz/' or 
                                    'https://xxxx.yy/zzz')
                                  """)

    args = parser.parse_args()
    start_url = args.START_URL
    job = args.job

    if job == 'path':
        end_url = args.END_URL
        shortest_path(start_url, end_url)
    if job == 'network':
        depth = args.depth
        scrap(start_url, depth)
