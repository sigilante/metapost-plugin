#!/usr/bin/env python3
"""Generate syntaxes/*.tmLanguage.json from the keyword lists below.

Edit the lists, then run:  python3 scripts/build-grammar.py
"""
import json
from pathlib import Path

# MetaPost tokens are runs of letters and underscores; digits start a new
# token (so `z1` is `z` followed by `1`). These guards replace `\b`.
B = r"(?<![A-Za-z_])"
E = r"(?![A-Za-z_])"

CONTROL = """
if elseif else fi for forsuffixes forever endfor exitif exitunless step until
upto downto begingroup endgroup input endinput end dump scantokens expandafter
within of
""".split()

DEFINITION = """
def vardef enddef primarydef secondarydef tertiarydef let newinternal save
interim delimiters outer inner
""".split()

TYPES = """
numeric pair path pen picture string transform color rgbcolor cmykcolor boolean
""".split()

PARAMETER_TYPES = "expr suffix text primary secondary tertiary".split()

# Statements and drawing commands (primitive, plain.mp, and plain.mf).
COMMANDS = """
beginfig endfig extra_beginfig extra_endfig draw fill filldraw unfill undraw
unfilldraw drawarrow drawdblarrow drawdot cutdraw drawoptions label dotlabel
labels dotlabels thelabel addto clip setbounds also contour doublepath withpen
withcolor withrgbcolor withcmykcolor withgreyscale withoutcolor withprescript
withpostscript dashed pickup shipout image message errmessage errhelp show
showtoken showvariable showdependencies showstats special fontmapfile
fontmapline readfrom write to closefrom randomseed everyjob filenametemplate
beginchar endchar penpos penstroke penlabels makelabel makeknown mode_setup
font_size font_slant font_normal_space font_normal_stretch font_normal_shrink
font_x_height font_quad font_extra_space define_pixels define_whole_pixels
define_whole_vertical_pixels define_good_x_pixels define_good_y_pixels
define_blacker_pixels define_whole_blacker_pixels define_corrected_pixels
define_horizontal_corrected_pixels lowres_fix ligtable charlist extensible
fontdimen headerbyte kern skipto boundarychar culldraw cull addto erase
openwindow display stop loggingall tracingall tracingnone incr decr
""".split()

# Operators and function-like macros.
FUNCTIONS = """
and or not abs angle arclength arctime ASCII char cosd sind decimal dir
direction directiontime directionpoint floor ceiling hex oct length mexp mlog
normaldeviate uniformdeviate point precontrol postcontrol reverse rotated
rotatedaround rotatedabout scaled shifted slanted transformed xscaled yscaled
zscaled reflectedabout sqrt substring subpath xpart ypart xxpart xypart yxpart
yypart redpart greenpart bluepart cyanpart magentapart yellowpart blackpart
greypart colormodel colorpart fontpart fontsize textpart pathpart penpart
dashpart makepath makepen intersectiontimes intersectionpoint unitvector round
max min mod div dotprod known unknown stroked filled textual clipped bounded
cycle curl tension controls atleast llcorner lrcorner ulcorner urcorner center
bbox buildcycle counterclockwise cutafter cutbefore interpath inverse magstep
penoffset softjoin takepower tensepath thru infont dashpattern on off
odd str top bot lft rt good hround vround
""".split()

CONSTANTS = """
true false nullpicture nullpen pencircle pensquare penrazor penspeck fullcircle
halfcircle quartercircle unitsquare identity origin up down left right
infinity epsilon whatever black white red green blue background evenly withdots
butt rounded squared mitered beveled currentpicture currentpen cuttings
ditto EOF
""".split()

UNITS = "mm cm pt bp in pc dd cc".split()

INTERNALS = """
ahangle ahlength bboxmargin charcode charext chardp charht charic charwd
day hour minute month year time defaultcolormodel defaultfont defaultpen
defaultscale dotlabeldiam labeloffset linecap linejoin miterlimit pausing
prologues showstopping truecorners warningcheck troffmode restoreclipcolor
hppp vppp mpprocset mpversion jobname numberprecision numbersystem
outputfilename outputformat outputformatoptions outputtemplate
tracingcapsules tracingchoices tracingcommands tracingequations
tracinglostchars tracingmacros tracingonline tracingoutput tracingrestores
tracingspecs tracingstats tracingtitles designsize fontmaking granularity
fillin smoothing autorounding turningcheck proofing xoffset yoffset
mode displaying currentwindow screen_rows screen_cols
blacker o_correction pixels_per_inch aspect_ratio
""".split()


def words(names):
    names = sorted(set(names), key=lambda s: (-len(s), s))
    return B + "(?:" + "|".join(names) + ")" + E


grammar = {
    "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
    "name": "MetaPost",
    "scopeName": "source.metapost",
    "patterns": [
        {"include": "#comment"},
        {"include": "#tex"},
        {"include": "#string"},
        {"include": "#definition"},
        {"include": "#input"},
        {"include": "#keywords"},
        {"include": "#number"},
        {"include": "#operator"},
        {"include": "#punctuation"},
    ],
    "repository": {
        "comment": {
            "match": "(%).*$",
            "name": "comment.line.percentage.metapost",
            "captures": {"1": {"name": "punctuation.definition.comment.metapost"}},
        },
        "string": {
            # MetaPost strings have no escapes and may not cross lines.
            "begin": '"',
            "end": '"|$',
            "name": "string.quoted.double.metapost",
            "beginCaptures": {"0": {"name": "punctuation.definition.string.begin.metapost"}},
            "endCaptures": {"0": {"name": "punctuation.definition.string.end.metapost"}},
        },
        "tex": {
            "begin": B + "(btex|verbatimtex)" + E,
            "end": B + "(etex)" + E,
            "beginCaptures": {"1": {"name": "keyword.control.tex.begin.metapost"}},
            "endCaptures": {"1": {"name": "keyword.control.tex.end.metapost"}},
            "contentName": "meta.embedded.block.latex",
            "patterns": [{"include": "text.tex.latex"}],
        },
        "definition": {
            # A macro header runs from `def`/`vardef` to the `=` (or `:=`) that
            # opens the body, possibly across several lines. Every plain
            # identifier inside it is a parameter name.
            "patterns": [
                {
                    "begin": B + r"(def|vardef)\s+([A-Za-z_]+)",
                    "beginCaptures": {
                        "1": {"name": "storage.type.function.metapost"},
                        "2": {"name": "entity.name.function.metapost"},
                    },
                    "end": r"(?=:?=)|(?=;)",
                    "name": "meta.function.header.metapost",
                    "patterns": [{"include": "#header"}],
                },
                {
                    "begin": B + r"(primarydef|secondarydef|tertiarydef)\s+([A-Za-z_]+)\s+([A-Za-z_]+|[^\sA-Za-z_0-9%;]+)",
                    "beginCaptures": {
                        "1": {"name": "storage.type.function.metapost"},
                        "2": {"name": "variable.parameter.metapost"},
                        "3": {"name": "entity.name.function.operator.metapost"},
                    },
                    "end": r"(?=:?=)|(?=;)",
                    "name": "meta.function.header.metapost",
                    "patterns": [{"include": "#header"}],
                },
            ]
        },
        "header": {
            "patterns": [
                {"include": "#comment"},
                {"match": words(PARAMETER_TYPES), "name": "storage.modifier.parameter.metapost"},
                {"match": r"@#|#@|(?<![A-Za-z_])@(?![A-Za-z_])", "name": "variable.parameter.suffix.metapost"},
                {"match": r"[A-Za-z_]+", "name": "variable.parameter.metapost"},
                {"include": "#punctuation"},
            ]
        },
        "input": {
            # `input` takes a bare file name, terminated by space, `;` or `%`.
            "match": B + r"(input)\s+([^\s;%\"]+)",
            "captures": {
                "1": {"name": "keyword.control.import.metapost"},
                "2": {"name": "string.unquoted.filename.metapost"},
            },
        },
        "keywords": {
            "patterns": [
                {"match": words(CONTROL), "name": "keyword.control.metapost"},
                {"match": words(DEFINITION), "name": "storage.type.function.metapost"},
                {"match": words(TYPES), "name": "storage.type.metapost"},
                {"match": words(PARAMETER_TYPES), "name": "storage.modifier.parameter.metapost"},
                {"match": words(CONSTANTS), "name": "constant.language.metapost"},
                {"match": words(INTERNALS), "name": "variable.language.internal.metapost"},
                {"match": words(COMMANDS), "name": "support.function.command.metapost"},
                {"match": words(FUNCTIONS), "name": "support.function.metapost"},
                {"match": r"@#|#@|(?<![A-Za-z_])@(?![A-Za-z_])", "name": "variable.parameter.suffix.metapost"},
                {"match": B + r"[xyz](?=\d)", "name": "variable.other.point.metapost"},
            ]
        },
        "number": {
            "patterns": [
                {
                    # A number immediately followed by a unit: 3mm, .5pt, 12bp
                    "match": r"(\d*\.\d+|\d+)(" + "|".join(UNITS) + ")" + E,
                    "captures": {
                        "1": {"name": "constant.numeric.metapost"},
                        "2": {"name": "keyword.other.unit.metapost"},
                    },
                },
                {"match": r"\d*\.\d+|\d+", "name": "constant.numeric.metapost"},
                {"match": words(UNITS), "name": "keyword.other.unit.metapost"},
            ]
        },
        "operator": {
            "patterns": [
                {"match": ":=", "name": "keyword.operator.assignment.metapost"},
                {"match": r"\.\.\.|\.\.|---|--|&", "name": "keyword.operator.path.metapost"},
                {"match": r"<>|<=|>=|=|<|>", "name": "keyword.operator.comparison.metapost"},
                {"match": r"\*\*|\+-\+|\+\+|[-+*/]", "name": "keyword.operator.arithmetic.metapost"},
                {"match": "#", "name": "keyword.operator.sharp.metapost"},
            ]
        },
        "punctuation": {
            "patterns": [
                {"match": ";", "name": "punctuation.terminator.statement.metapost"},
                {"match": ",", "name": "punctuation.separator.metapost"},
                {"match": ":", "name": "punctuation.separator.colon.metapost"},
            ]
        },
    },
}

metafont = {
    "$schema": grammar["$schema"],
    "name": "METAFONT",
    "scopeName": "source.metafont",
    "patterns": [{"include": "source.metapost"}],
}

out = Path(__file__).resolve().parent.parent / "syntaxes"
for name, data in [("metapost", grammar), ("metafont", metafont)]:
    path = out / f"{name}.tmLanguage.json"
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {path}")
