from pathlib import Path
from fontParts.world import OpenFont

rootDir = Path(__file__).parent.parent
testsDir = rootDir / "tests"
UFOpath = testsDir / "_.ufo"
font = OpenFont(UFOpath)
glyph = font["test02"]
refLine = (-50, -100), (600, 60)
glyph.naked().getRepresentation("doodle.Beam", beam=refLine, canHaveComponent=False)
