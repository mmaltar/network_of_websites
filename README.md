# network of websites - web scraping & memgraph database script

## Running

```
python main.py network START_URL [--depth | -d DEPTH]
python main.py path START_URL END_URL
```
Database host and port for mgclient are set in the settings.py.

## Dependencies

[mgclient](https://github.com/memgraph/mgclient) <br>
[pymgclient](https://github.com/memgraph/pymgclient) <br>
[requests](https://pypi.org/project/requests/2.7.0/) <br>
[beautifulsoup4](https://pypi.org/project/beautifulsoup4/)


