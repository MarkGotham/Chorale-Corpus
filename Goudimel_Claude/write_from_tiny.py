# -*- coding: utf-8 -*-
"""
NAME
===============================
Write from Tiny (write_from_tiny.py)


BY:
===============================
Mark Gotham


LICENCE:
===============================
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================
Write score from the tiny notation and associated metadata in the central json doc.


"""

import json
from music21 import clef, converter, expressions, key, metadata, meter, stream
import os


orig_part_list = ["superius", "contra", "tenor", "bassus"]
mod_part_list = ["S", "A", "T", "B"]
mod_to_orig_map = [2, 0, 1, 3]  # ["S": "tenor", "A": "superius", "T":"contra", "B": "bassus"]


def corpus_from_json_tiny(
        write_ancient: bool = True,
) -> None:
    with open("./goudimel.json", "r") as data:
        data = json.load(data)
        for item in data:
            print(item["psalm_number"])
            psalm_number = str(item["psalm_number"]).zfill(3)
            if "superius" in item:  # ready to go
                if write_ancient:
                    write_from_tiny(item)
            else:
                print("No copy of psalm number", psalm_number)


def write_from_tiny(
        data: dict,
) -> stream.Score:
    """Write one ancient version of a score from the json tinyNotation."""
    s = stream.Score()
    for i in range(len(orig_part_list)):
        name = orig_part_list[i]
        p = converter.parse(data[name])
        p.partName = name

        # Clef
        c = p.recurse().getElementsByClass(clef.Clef).first()
        c.sign = data["clefs"][i][0]
        c.line = int(data["clefs"][i][1])
        p.insert(0, c)

        # Key signature
        if data["orig_key"]:
            p.insert(0, key.KeySignature(-1))  # always one flat or nothing

        # Time signature display symbol
        p.recurse().getElementsByClass(meter.TimeSignature).first().symbol = "cut"  # here, not supported in tiny

        # Last note. Special case due to tiny notation encoding.
        last_note = p.recurse().notesAndRests[-1]
        # last_note.duration.quarterLength = 8  # Either this double length (if so, also move the double barline).
        last_note.expressions.append(expressions.Fermata())  # Or this.

        p.makeMeasures(inPlace=True)
        p.makeTies(inPlace=True)

        s.insert(p)

    psalm_number = str(data["psalm_number"])
    s.insert(0, metadata.Metadata())
    s.metadata.title = f'Psalm {psalm_number}: {data["title"]}'
    s.metadata.composer = 'Claude Goudimel'

    psalm_number = psalm_number.zfill(3)
    out_path = os.path.join('.', 'Pseaumes', psalm_number, f"Goudimel_{psalm_number}_original.mxl")
    s.write("mxl", out_path)

    return s


if __name__ == '__main__':
    corpus_from_json_tiny()
