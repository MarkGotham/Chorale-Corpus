"""
Prepare the individual Bach chorales from the combined source.
"""

from music21 import clef, converter, key, metadata, meter, stream
from pathlib import Path
from copy import deepcopy

import catalogue_working

THIS_FOLDER = Path(__file__).parent


class SegmentScore:
    """
    Initialises with a score to be segmented and processed in other ways.
    """

    def __init__(self, file_name: str = "1-120.mxl"):

        # Inits
        self.end_chorale = None
        self.start_chorale = None
        self.num_chorales = None
        self.start_measures = []
        self.missing = []
        self.extra = []
        self.metadata_errors = None
        self.current_segment = None
        # self.current_segment_open = None  # TODO
        self.current_work_number = None

        # Processes
        self.file_name = file_name
        self.path_to_score = THIS_FOLDER / file_name
        self.num_from_title()
        self.score = converter.parse(self.path_to_score)
        self.no_stem_dir()
        self.renumber_and_find_break()
        self.segment_source()
        if self.metadata_errors:
            print(f"Error getting metadata for chorales number {self.metadata_errors}")

    def num_from_title(self):

        # Special case of test files (chorales 1–3)
        if self.file_name == "test.mxl":
            self.num_chorales = 3
            self.current_work_number = 1
            return

        a, b = self.file_name.split(".")[0].split("-")
        self.start_chorale = int(a)
        self.end_chorale = int(b)
        self.num_chorales = self.end_chorale - self.start_chorale + 1
        self.current_work_number = self.start_chorale

    def no_stem_dir(self):
        """
        Remove stem direction on all notes to support short and open scoring.
        """
        for n in self.score.recurse().notes:
            n.stemDirection = None

    def renumber_and_find_break(self):
        """
        Renumber:
        The source numbers measures for each chorale from 1,
        That would be helpful for segmentation,
        except that the music21 measures() method expects
        measure numbers for arguments and with multiple sections,
        each starting from number 1, that is obviously not going to work.
        So we number each measure 1, 2, 3, and so on
        (self.re_number fixes this again at the end).

        Find break:
        While renumbering, store these breaks points between chorale
        indicated by the measure number re-start.
        Tests indicate that the measure re-start is reliable and that
        there are also clef changes at all and only such moments.
        Key and time signatures are almost but not quite so reliable.
        This method prints all such deviations as
        - `missing` where break points do not have a change of clef, key, and meter
        - `extra` where for other points that do have those changes.

        """

        for i in range(2):
            self.run_one_part(part_num=i)

    def run_one_part(self, part_num: int):
        """
        Sub-method for `renumber_and_find_break` on each part.
        """

        previous_run = None

        # Prints both parts, but attribute end up with one part worth of info here.
        self.missing = {"key signature": [],
                        "time signature": [],
                        "clef": []
                        }
        self.extra = {"key signature": [],
                      "time signature": [],
                      "clef": []
                      }

        if self.start_measures:
            previous_run = self.start_measures
            self.start_measures = []

        last_measure_number = 100  # anything > 1 really ...
        count = 1
        for m in self.score.parts[part_num].getElementsByClass(stream.Measure):
            if m.number < last_measure_number:  # new chorale: Should be changes on all classes
                self.start_measures.append(count)
                if not m.getElementsByClass(key.KeySignature):
                    self.missing["key signature"].append(count)
                if not m.getElementsByClass(meter.TimeSignature):
                    self.missing["time signature"].append(count)
                if not m.getElementsByClass(clef.Clef):
                    self.missing["clef"].append(count)

            else:  # cont. chorale: Should be no class changes
                if m.getElementsByClass(key.KeySignature):
                    self.extra["key signature"].append(count)
                if m.getElementsByClass(meter.TimeSignature):
                    self.extra["time signature"].append(count)
                if m.getElementsByClass(clef.Clef):
                    self.extra["clef"].append(count)

            # all cases
            last_measure_number = m.number  # NB: before next line
            m.number = count
            count += 1

        print("*** Warnings ***")
        if self.missing:
            print("Missing:")
            for m in self.missing:
                if self.missing[m]:
                    print(f"{m} in measures {self.missing[m]}")
        if self.extra:
            print("Extra:")
            for e in self.extra:
                if self.extra[e]:
                    print(f"{e} in measures {self.extra[e]}")

        assert (self.num_chorales == len(self.start_measures))

        if previous_run and (previous_run != self.start_measures):
            print("Difference between the parts:")
            print(previous_run)
            print(self.start_measures)

    def segment_source(self):
        """
        Segment the Bach chorale source into separate chorales
        using the break points found in `renumber_and_find_break`.
        """

        for index in range(len(self.start_measures[:-1])):
            start = self.start_measures[index]
            end = self.start_measures[index + 1] - 1
            self.current_segment = deepcopy(self.score.measures(start, end))
            self.write_segment()

            # Re-init
            self.current_work_number += 1

        # Last one
        start = self.start_measures[-1]
        self.current_segment = deepcopy(self.score.measures(start, start + 50))
        self.write_segment()

        assert (self.current_work_number == self.end_chorale)

    def write_segment(self):
        """
        Write segment including metadata (for which see `prep_metadata`).

        TODO: both short (2-stave) and open (4-stave) settings.
        """

        print(f"Processing number {self.current_work_number} ...")
        print("Before: ", self.current_work_number)
        r_number = catalogue_working.map_to_Riemenschneider(self.current_work_number)
        print("After: ", r_number)

        out_path = THIS_FOLDER.parent / "Chorales" / str(r_number).zfill(3)

        # TODO: Open scoring version *
        # self.current_segment_open = self.current_segment.voicesToParts()
        # self.current_segment_open.parts[2].insert(0, clef.Treble8vbClef())

        self.part_names()

        self.prep_metadata(r_number)  # Metadata not kept in voicesToParts

        for p in self.current_segment.parts:
            re_number(p)

        self.current_segment.write(fmt="mxl", fp=out_path / "short_score.mxl")

        print("... done")

    def part_names(self):
        self.current_segment.parts[0].partName = "S,A"
        self.current_segment.parts[1].partName = "T,B"

        # TODO open *
        # satb = "SATB"
        # for index in range(len(satb)):
        #     self.current_segment_open.parts[index].partName = satb[index]

    def prep_metadata(self, riemenschneider_number: int):
        """
        Prepare the metadata on the current segment:
        composer and "title".
        Title = the deduced Riemenschneider number (1–371) and corresponding text.
        """

        self.current_segment.insert(0, metadata.Metadata())

        self.current_segment.metadata.composer = "J. S. Bach"

        catalogue_title = catalogue_working.catalogue[riemenschneider_number - 1][1]
        title = f"Chorale {riemenschneider_number}:\n{catalogue_title}"

        self.current_segment.metadata.title = title


def re_number(this_part: stream.Part):
    """
    Re_number the measures of a part according to standard practice:
    - (optional) anacrusis = 0
    - Then 1, 2, 3
    - Split measures numbered Xa, Xb
    """
    measures = this_part.recurse().getElementsByClass(stream.Measure)

    if measures[0].duration.quarterLength == measures[0].barDuration.quarterLength:
        count = 1
    else:
        count = 0

    measures[0].number = count

    for msr in measures[1:-1]:
        count += 1
        # If actual (duration) = nominal (barDuration)
        if msr.duration == msr.barDuration:
            # simply, complete measure. Iterate
            msr.number = count
        else:
            if msr.duration.quarterLength + msr.next().duration.quarterLength == \
                    msr.barDuration.quarterLength:
                # split measure:
                msr.number = count
                msr.numberSuffix = "a"
                msr.next().number = count
                msr.next().numberSuffix = "b"
            # else no action - e.g., sees Xb twice and should not re-number

    # last measure
    measures[-1].number = count + 1

# TODO open *
# def check_exactly_2_voices(self):
#     """
#     In preparation for the open score version, check that there are
#     exactly 2 voices in each part / measure.
#     """
#     msrs = self.score.recurse().getElementsByClass(stream.Measure)
#     for m in msrs:
#         if len(m.voices) != 2:
#             raise ValueError(f"More than 2 voices in {m.measureNumber}")


def process_corpus():
    for range_string in ("1-120", "121-240", "241-371",):
        SegmentScore(file_name=range_string + ".mxl")


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    process_corpus()
