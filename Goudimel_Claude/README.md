# Goudimel, Claude: The Geneva Psalter

A selection of 41 near-homophonic Psalms from the "Genevan Psalter" collection.
These 41 were selected to provide the corresponding scores 
for harmonic analyses originally by Dmitri Tymoczko and provided on the
[When in Rome meta-corpus of harmonic analysis](https://github.com/MarkGotham/When-in-Rome/tree/master/Corpus/Early_Choral/Goudimel%2C_Claude/Psalmes).
As the keys and time values differ, this source records the original in music21's `tinyNotation`
along with the transpositions needed to match DT's analyses.
Both "ancient" and "modern" versions of the scores (generated from the json)
are provided here.
More details follow below.


## External, Original Source, 1564

The source for this transcription is the earliest available on IMSLP:
[the 2nd edition, of 1564, here](https://imslp.org/wiki/150_Pseaumes_de_David,_1564_(Goudimel,_Claude))
This leads to two files for the:
- [first half here (1-68)](https://s9.imslp.org/files/imglnks/usimg/f/f2/IMSLP498673-PMLP572700-Les_Pseaumes_mis_en_rime_1565_Goudimel_Claude_btv1b525015926_1-68.pdf)
- [second half here (69-150)](https://ks15.imslp.org/files/imglnks/usimg/1/1f/IMSLP498674-PMLP572700-Les_Pseaumes_mis_en_rime_1565_Goudimel_Claude_btv1b525015926_69-150.pdf)

This source's frontispiece describes it as:

```
LES
PSEAUMES MIS
EN RIEM FRAN-
SCOISE,
PAR CLEMENT MAROT ET
Theodore de Beze.
MIS EN MUSIQUE A QUATRE
parties par Claude Goudimel.
[...]
M.D.LXV
```

Yes, the captilisation really is like that. ;)

Note also that IMSLP provides a
[comparison of sources using the Genevan Psalter melodies here.]
(https://imslp.org/wiki/List_of_collections_containing_the_Genevan_Psalter_melodies)

This original source is set out in the "Choirbook format" that was common at the time.
This allows for all four voices to read from the same double page.
This layout is neither like the modern score (all parts together) nor modern parts (all parts on separate documents).
Perhaps the closest modern equivalent is the four-hands piano format where two players (primo and secondo)
play from on the same piano and read from the same double page.


## Local encodings ... on json

In describing this repo, we begin with the main point of reference
from which all secondary sources automatically derive: `goudimel.json`.
This contains the following keys for _all_ 150:
- `title`: `str`, Original French titles (note the old language and spelling) that sets the file's alphabetical order.
- `psalm_number`: int, 1-150.
- original and modern keys
- string (text) representations of the original parts in music21's tinyNotation.
	- this covers all relevant data except the following which we also provide on the json:
- `mod sharps`
- `orig_bass`: `str` for a pitch name with octave (e.g, "C4" - not to be confused with the clefs).
- `orig_key`: The original key signature expressed as a bool: there is either no key signature or one of a single flat.
- `orig_clefs`: a list of four entries, specifying the `sign` and `line` of the clefs in the original parts (from superius to basses). E.g., ["G2", "C3", "C3", "F4"].

Additionally, for the 41 transcribed so far, there are the following keys:
- `mod_trans`: the number of semitones and direction (+/-) for transposing from the original to the modern key choice.
- `mod_sharps`: the time signature of a typical modern version expressed as a number of sharps. Note that this cannot be deduced from the transposition as we are dealing with modal sources.
- `superius`, `contra`, `tenor`, `bassus`

## Local encodings ... in mxl

From the json data, the code renders scores in both "original" and "modern" versions.

"Original" here means that it follows the source in terms of:
- open score with one voice part per stave, (though the original is in the "Choirbook format" as discussed above)
- part names: "superius", "contra", "tenor", "bassus"
- clefs: including C-clefs like "soprano", "alto", "tenor".
- note values, moving mostly in whole notes.
- part distribution with the cantus firmus melody that Goudimel harmonised placed in the tenor (middle of the texture)
- transposition level

The original is almost entirely expressed in the json, with the exception of elements unsupported by tiny notation:
- Final notes are usual double the length.
  - Here we add a fermata.
  - Alternatives include doubling the length on rendering
- This range of clefs is not supported. They are added from data in the json.
- time signature symbol. Tiny notation supports the concept of `2/2` but the symbol is added later.

"modern" means
- still open score (though with a script provided to adapt to short score)
- modern part names: SATB
- modern clefs: treble, treble, treble8, bass
- tenor cantus firmus moved to the top 
- halved note values
- transposed to keys match up with the harmonic analyses on [When in Rome](https://github.com/MarkGotham/When-in-Rome/tree/master/Corpus/Early_Choral/Goudimel%2C_Claude/Psalmes)


## Scripts

The code here serves to:
- `write_from_tiny`: render scores in self-explanatory ways.
- `corpus_conversion`: use musescore to convert between any supported formats
- `clef_tree`: produce a summary of clefs used and their counts as below

```
.
├── superius:C1
│   ├── contra:C2 = C1,C2
│   │   ├── tenor:C3 = C1,C2,C3
│   │   │   └── bassus:F3 = C1,C2,C3,F3 = 1
│   │   └── tenor:C4 = C1,C2,C4
│   │       └── bassus:F3 = C1,C2,C4,F3 = 1
│   └── contra:C3 = C1,C3
│       └── tenor:C4 = C1,C3,C4
│           ├── bassus:C4 = C1,C3,C4,C4 = 1
│           ├── bassus:F3 = C1,C3,C4,F3 = 1
│           └── bassus:F4 = C1,C3,C4,F4 = 88
└── superius:G2
    ├── contra:C2 = G2,C2
    │   ├── tenor:C3 = G2,C2,C3
    │   │   ├── bassus:C4 = G2,C2,C3,C4 = 14
    │   │   ├── bassus:F3 = G2,C2,C3,F3 = 41
    │   │   └── bassus:F4 = G2,C2,C3,F4 = 1
    │   └── tenor:C4 = G2,C2,C4
    │       └── bassus:F3 = G2,C2,C4,F3 = 1
    └── contra:C3 = G2,C3
        ├── tenor:C3 = G2,C3,C3
        │   └── bassus:F3 = G2,C3,C3,F3 = 2
        └── tenor:C4 = G2,C3,C4
            └── bassus:F4 = G2,C3,C4,F4 = 1
```
