#! /usr/bin/env python3

"""python program to solve the world problems..."""

import os, sys, string, time, logging, argparse
import re
import logging

import svgutil

_version = "0.1"

import rectpack

from lxml import etree as et
from lxml import builder

svg_ns = 'http://www.w3.org/2000/svg'

class Part:
  def __init__(self):
    self.size = None
    self.scale = None
    self.viewbox = None
    self.bbox = None
    self.rotated = False

    self.tree = None

def parseSVGs(files):
  defpat = re.compile("<defs>(.+)</defs>", re.DOTALL)
  drawpat = re.compile("(<g id=.+)</svg>", re.DOTALL)

  viewboxpat = re.compile('viewBox="(\d+) (\d+) (\d+) (\d+)"')
  dimpat = re.compile('width="(\d+)mm" height="(\d+)mm"')

  parts = []

  for n, fn in enumerate(files):
    prefix = "%d:%s" % (n, fn)
    logging.debug("processing %s" % prefix)

    parser = et.XMLParser(remove_blank_text=True)
    src_tree = et.parse(fn, parser)

    part = Part()
    parts.append(part)

    part.size = svgutil.getSizeInMM(src_tree)
    part.scale = svgutil.ticksPerMM(src_tree)
    part.viewbox = svgutil.getViewBox(src_tree)
    part.bbox = (part.viewbox[2], part.viewbox[3])

    part.tree = src_tree

    logging.debug(prefix + ": size:%s viewbox:%s scale:%s" % (part.size, part.viewbox, part.scale))

  return parts

def layoutParts(parts, viewport_size, margin=4, outermargin=10):
  packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline, rotation=True)
  #packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline, rotation=False)

  for n,part in enumerate(parts):
    rid = packer.add_rect(part.bbox[0]+margin, part.bbox[1]+margin, n)

  packer.add_bin(viewport_size[0]-outermargin*2, viewport_size[1]-outermargin*2, count=float("inf"))

  packer.pack()

  pages = []

  for abin in packer:
    logging.debug("packed %d of %d parts" % (len(abin), len(parts)))
    page = []
    pages.append(page)
    for rect in abin:
      part = parts[rect.rid]
      page.append(part)
      part.x = rect.x+margin//2
      part.y = rect.y+margin//2

      rratio = rect.width / rect.height
      pratio = part.bbox[0] / part.bbox[1]

      dr = abs(rratio - pratio)

      if dr > 0.1:
        part.rotated = True
  return pages

def writeSVG(outfn, parts, viewport_size, margin=5, outermargin=10, units="mm"):
  minx = 12000
  miny = 12000
  vp_max_width = 0
  vp_max_height = 0
  dimx = 0
  dimy = 0

  for n,part in enumerate(parts):
    minx = min(minx, part.x)
    miny = min(miny, part.y)

    dimx += part.bbox[0]
    dimy = max(dimy, part.bbox[1])

    vp_max_width = max(vp_max_width, part.viewbox[2])
    vp_max_height = max(vp_max_height, part.viewbox[3])

  #logging.debug("minx:%s miny:%s" % (minx, miny))

  miny = 9400

  fp = open(outfn, "w")
  fp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
  fp.write('<svg xmlns="http://www.w3.org/2000/svg"\n')
  fp.write('  xmlns:xlink="http://www.w3.org/1999/xlink"\n')
  fp.write('  xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"\n')
  fp.write('  xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n')
  fp.write('  sodipodi:docname="box.svg"\n')

  fp.write('  width="%d%s" height="%d%s"\n' % (viewport_size[0], units, viewport_size[1], units))
  viewBox = (minx-outermargin*2, miny+outermargin, viewport_size[0], viewport_size[1])
  fp.write('  viewBox="%d %d %d %d"\n' % viewBox)
  fp.write('  version="1.1">\n')

  fp.write('<sodipodi:namedview id="namedview312" inkscape:document-units="%s" />\n' % units)
  fp.write("</svg>\n")
  fp.close()
  
  parser = et.XMLParser(remove_blank_text=True)
  body = open(outfn, "r")
  dest_tree = et.parse(outfn, parser)
  dest_root = dest_tree.getroot()

  xlink = '{http://www.w3.org/1999/xlink}href'
  crosses = []
  for n, part in enumerate(parts):
    for el in part.tree.getroot():
      dest_root.append(el)

      cx = viewBox[0]+part.x + margin + part.bbox[0]//2
      cy = viewBox[1]+viewBox[3]-part.y - margin - part.bbox[1]//2
      #crosses.append(cross((cx, cy), 10))

      cx = viewBox[0]+part.x + margin
      cy = viewBox[1]+viewBox[3]-part.y - margin 
      crosses.append(cross((cx, cy), 10))

      if el.tag.endswith("g"):
        if part.rotated:
          rotation = 90
          el.set("transform", 'rotate(%d %d %d) translate(%d %d)' % (rotation, 
                                                                     cx, cy,
                                                                     part.x - part.bbox[0], -part.y))
        else:
          el.set("transform", 'translate(%d %d)' % (part.x, -part.y))
      elif el.tag.endswith("defs"):
        for child in el.iterfind(".//{%s}symbol" % svg_ns):
          child.attrib['id'] = child.attrib['id'].replace("glyph", "glyph%d_" % n)
      for child in el.iterfind(".//{%s}use" % svg_ns):
        if xlink in child.attrib:
          child.attrib[xlink] = child.attrib[xlink].replace("glyph", "glyph%d_" % n)

  if 0:
    E = builder.ElementMaker(namespace=svg_ns)
    group = E.g(transform="translate(%d %d)" % (outermargin, outermargin))
    dest_root.insert(0, group)

  if 0:
    for _cross in crosses:
      dest_root.append(_cross)

  if 0:
    dest_root.append(cross((0,0)))
    dest_root.append(cross((viewBox[0], viewBox[1])))
    dest_root.append(cross((viewBox[0]+viewBox[2], viewBox[1])))
    dest_root.append(cross((viewBox[0]+viewBox[2], viewBox[1]+viewBox[3])))
    dest_root.append(cross((viewBox[0], viewBox[1]+viewBox[3])))

  et.ElementTree(dest_root).write(outfn, pretty_print=True, encoding='utf-8', xml_declaration=True)

def cross(pos, size=50):
  E = builder.ElementMaker(namespace=svg_ns)
  group = E.g()
  group.append(E.line(x1=str(pos[0]-size), y1=str(pos[1]), x2=str(pos[0]+size), y2=str(pos[1]), style="stroke:rgb(255,0,0);stroke-width:2"))
  group.append(E.line(x1=str(pos[0]), y1=str(pos[1]-size), x2=str(pos[0]), y2=str(pos[1]+size), style="stroke:rgb(255,0,0);stroke-width:2"))
  return group
  

def mergeSVG(outfn, viewport_size, files, margin=2, outermargin=5, units="mm"):
  parts = parseSVGs(files)

  pages = layoutParts(parts, viewport_size, margin)

  if len(pages) > 1:
    _fn, _ext = os.path.splitext(outfn)
    outfn = "%s\%d.%s" % (_fn, _ext)

  for pagenum,_parts in enumerate(pages):
    try:
      fn = outfn % pagenum
    except TypeError:
      fn = outfn
    logging.debug("writing SVG %s" % fn)
    writeSVG(fn, _parts, viewport_size, margin, outermargin, units)

def start(args):
  outfn = "box.svg"

  mergeSVG(outfn, (1220, 609), args.files)

def test():
  logging.warn("Testing")

def parse_args(argv):
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description=__doc__)

  parser.add_argument("-t", "--test", dest="test_flag", 
                    default=False,
                    action="store_true",
                    help="Run test function")
  parser.add_argument("--log-level", type=str,
                      choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                      help="Desired console log level")
  parser.add_argument("-d", "--debug", dest="log_level", action="store_const",
                      const="DEBUG",
                      help="Activate debugging")
  parser.add_argument("-q", "--quiet", dest="log_level", action="store_const",
                      const="CRITICAL",
                      help="Quite mode")
  parser.add_argument("files", type=str, nargs='+')

  args = parser.parse_args(argv[1:])

  return parser, args

def main(argv, stdout, environ):
  if sys.version_info < (3, 0): reload(sys); sys.setdefaultencoding('utf8')

  parser, args = parse_args(argv)

  logging.basicConfig(format="[%(asctime)s] %(levelname)-8s %(message)s", 
                    datefmt="%m/%d %H:%M:%S", level=args.log_level)

  if args.test_flag:  test();   return

  start(args)

if __name__ == "__main__":
  main(sys.argv, sys.stdout, os.environ)
