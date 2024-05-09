# -*- coding: utf-8 -*-
"""
NAME
===============================
Corpus Conversion (corpus_conversion.py)

BY:
===============================
Mark Gotham


LICENCE:
===============================
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================
Script to make/update the `corpus_conversion.json` file to support batch convertion.
Similar routine as: `https://github.com/OpenScore/Lieder/blob/main/README.md`
and same notes as there.

"""

import json
import os


def prep_conversion_doc(
        write: bool = False,
        in_format: str = ".mxl",
        out_format: str = ".mscz"
) -> None:
    """
    Prepare a list of dicts with in / out paths of proposed conversions
    and (optionally) write to a `corpus_conversion.json` file in this folder.
    """

    if out_format not in [".mxl", ".pdf", ".mid", ".mscz", ".mscx"]:
        raise ValueError("Invalid out_format")

    out_data = []
    for psalm_number in [
        1, 3, 21, 25, 29, 32, 35, 36, 42, 43, 47, 49,
        52, 54, 56, 60, 66, 68, 73, 75, 79, 81, 84, 89, 97, 98, 99,
        101, 105, 108, 118, 119, 122, 123, 124, 127, 133, 135, 138, 140, 150
    ]:
        psalm_number = str(psalm_number).zfill(3)
        basic_path = os.path.join(".", "Pseaumes", psalm_number, f"Goudimel_{psalm_number}_original")
        x = {
            "in": basic_path + in_format,
            "out": basic_path + out_format
        }
        out_data.append(x)

    if write:
        out_path = os.path.join(".", "corpus_conversion.json")
        with open(out_path, "w") as json_file:
            json.dump(out_data, json_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    prep_conversion_doc(write=True)
