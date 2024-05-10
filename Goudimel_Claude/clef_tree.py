# -*- coding: utf-8 -*-
"""
NAME
===============================
Clef Tree (clef_tree.py)


BY:
===============================
Mark Gotham


LICENCE:
===============================
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================
Quick demo to show the choices of clefs in tree format.

"""

import json
from collections import Counter
from treelib import Tree


orig_part_list = ["superius", "contra", "tenor", "bassus"]


def process_corpus() -> None:
    """
    Run `split_part` on the full corpus and write.
    """
    with open("./goudimel.json", "r") as data:  # Hardcoded path
        data = json.load(data)
        clef_lists = [item["clefs"] for item in data]
        distinct_with_count = Counter(["-".join(c) for c in clef_lists])
        tree = Tree()
        tree.create_node(".", ".")

        for x in distinct_with_count.keys():  # e.g., 'C1-C3-C4-F3'
            clef_list = x.split("-")  # e.g., ['C1', 'C3', 'C4', 'F4']

            i = 0  # "superius"
            if clef_list[i] not in tree:
                tree.create_node(
                    orig_part_list[i] + ":" + clef_list[i],  # display. e.g., "superius:C1"
                    clef_list[i],  # this ref, e.g., "C1"
                    parent="."  # parent ref
                )

            # i=1,2 for "contra" and "tenor"
            for i in range(1, 3):
                so_far = ",".join(clef_list[0:i])
                so_far_and_now = ",".join(clef_list[0:i+1])
                if so_far_and_now not in tree:
                    tree.create_node(
                        f"{orig_part_list[i]}:{clef_list[i]} = {so_far_and_now}",
                        so_far_and_now,  # NB
                        parent=so_far
                    )

            i = 3  # "bassus"
            so_far = ",".join(clef_list[0:i])
            so_far_and_now = ",".join(clef_list)  # [0:i + 1]
            if so_far_and_now not in tree:
                tree.create_node(
                    f"{orig_part_list[i]}:{clef_list[i]} = {so_far_and_now} = {distinct_with_count[x]}",
                    parent=so_far
                )

        tree.show()


if __name__ == '__main__':
    process_corpus()
