import datetime, os, tempfile
from tap_rest_api import sync
from tap_rest_api.schema import infer_schema
from tap_rest_api.helper import Stream, remove_datetime_format
from singer import utils
from singer.catalog import Catalog


def _prep_config():
    cwd, _ = os.path.split(__file__)
    usgs_dir = os.path.join(cwd, "../examples/usgs")
    config = utils.load_json(os.path.join(usgs_dir, "config/tap_config.json"))
    config["schema_dir"] = os.path.join(usgs_dir, "schema")
    config["catalog_dir"] = os.path.join(usgs_dir, "catalog")
    catalog = Catalog.load(os.path.join(usgs_dir, config["catalog_dir"],
                                        "earthquakes.json"))
    config["start_datetime"] = (datetime.datetime.now() -
                                datetime.timedelta(hours=1)).isoformat()
    streams = {}
    streams["earthquakes"] = Stream("earthquakes", config)
    return config, catalog, streams


# def test_infer_schema():
#     config, catalog, streams = _prep_config()
#     with tempfile.TemporaryDirectory() as build_dir:
#         config["schema_dir"] = build_dir
#         config["catalog_dir"] = build_dir
#         infer_schema(config, streams)


def test_sync():
    config, catalog, streams = _prep_config()
    state = {}
    sync(config, streams, state, catalog, auth_method="no_auth")

def test_remove_date_time_format():
    data = {
        "name": "John",
        "format": "date-time",
        "metadata": {
            "format": "date-time",
            "age": 30,
            "address": {
                "format": "string",
                "city": "New York"
            }
        },
        "siblings": [
            {
                "name": "Jane",
                "format": "date-time"
            },
            {
                "name": "Joe",
                "format": "string"
            }
        ]
    }

    remove_datetime_format(data)

    assert data.get("format") is None
    assert data["metadata"].get("format") is None
    assert data["siblings"][0].get("format") is None
    assert data["siblings"][1].get("format") is "string"

