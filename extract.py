"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, "r") as infile:
        reader = csv.DictReader(infile)
        neos = []
        for line in reader:
            line["name"] = line["name"] or None
            line["diameter"] = float(line["diameter"]) if line["diameter"] else None
            line["pha"] = False if line["pha"] in ["N", ""] else True

            try:
                neo = NearEarthObject(pdes=line["pdes"],
                                      name=line["name"],
                                      diameter=line["diameter"],
                                      pha=line["pha"])
            except Exception as e_csv:
                print(e_csv)
            else:
                neos.append(neo)

    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, "r") as infile:
        reader = json.load(infile)
        reader = [dict(zip(reader["fields"], data)) for data in reader["data"]]
        close_approaches = []

        for line in reader:
            try:
                approach = CloseApproach(des=line["des"],
                                         cd=line["cd"],
                                         dist=float(line["dist"]),
                                         v_rel=float(line["v_rel"]))
            except Exception as e_json:
                print(e_json)
            else:
                close_approaches.append(approach)
    return close_approaches
