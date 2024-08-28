# -*- coding: utf-8 -*-
"""
NAME
===============================
Write to Tiny (write_to_tiny.py)


BY:
===============================
Mark Gotham


LICENCE:
===============================
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================
Although this repo works by
storing the VoR in JSON as strings and
creating scores in mxl format from there,
often it's easier to
create some version of the scores in a music notation editor first and
extract at least an initial version of the string representation from there.
These initial scores can be then discarded.
This module helps with that process by writing from score to tiny notation strings.
"""

from __future__ import annotations
from music21 import converter, note, pitch, stream


def tiny_pitch(p: pitch.Pitch):
    """
    Writes music21 tiny notation for a single note where the octaves are specified as follows:
    CC to BB for octave 2,
    C to B for octave 3,
    c  to b for octave 4,
    and
    c' to b' for octave 5.

    >>> [tiny_pitch(pitch.Pitch(p)) for p in ["C2", "C3", "C4", "C5"]]
    ['CC', 'C', 'c', "c'"]


    Special attention to flats:
    >>> tiny_pitch(pitch.Pitch("B-2"))
    'BB-'

    """
    out_string = p.name  # NB no octave
    if p.octave == 2:
        # in case of p.accidental, but works anyway
        return out_string[0] + out_string
    elif p.octave == 3:
        return out_string  # no change, .upper() is default
    elif p.octave == 4:
        return out_string.lower()
    elif p.octave == 5:
        if len(out_string) > 1:
            return out_string[0].lower() + "'" + out_string[1:]  # : in case of double sharp/flat ##
        else:
            return out_string.lower() + "'"
    else:
        raise ValueError(f"Only octaves in the range 2–-5 are supported: {p.nameWithOctave} is outside this range.")


tiny_duration = {  # better than a function: KeyError fail if the value is unrecognised (rather that changing it).
    6: "1.",
    4: "1",
    3: "2.",
    2: "2",
    1.5: "4.",
    1: "4",
    0.75: "8.",
    0.5: "8",
    0.25: "16",
}  # all used in this repertoire


def part_to_tiny(
        p: stream.Part,
        t: int | None = None
) -> str:

    out_string = "tinyNotation: 2/2 "  # "cut" not supported
    last_ql = None

    for n in p.stripTies().recurse().notesAndRests:

        this_ql = n.duration.quarterLength

        # Pitch / rest
        if n.isRest:
            out_string += "r"
        else:
            p = n.pitch
            p.transpose(t, inPlace=True)
            out_string += tiny_pitch(n)

        # Duration
        if this_ql != last_ql:
            out_string += tiny_duration[this_ql]
            last_ql = this_ql

        out_string += " "

    return out_string


if __name__ == '__main__':
    import doctest
    doctest.testmod()
