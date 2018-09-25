#! /usr/bin/env python3

"""python program to solve the world problems..."""

import os, sys, string, time, logging, argparse
import re
import logging

_version = "0.1"

import rectpack

def parseSVGs(files):
  defpat = re.compile("<defs>(.+)</defs>", re.DOTALL)
  drawpat = re.compile("(<g id=.+)</svg>", re.DOTALL)

  viewboxpat = re.compile('viewBox="(\d+) (\d+) (\d+) (\d+)"')
  dimpat = re.compile('width="(\d+)mm" height="(\d+)mm"')

  parts = []

  for n, fn in enumerate(files):
    prefix = "%d:%s" % (n, fn)
    logging.debug("processing %s" % prefix)
    body = open(fn, "r").read()

    part = {}
    parts.append(part)
    part['rotated'] = False

    m = viewboxpat.search(body)
    if m:
      part['vp_minx'] = int(m.group(1))
      part['vp_miny'] = int(m.group(2))
      part['vp_width'] = int(m.group(3))
      part['vp_height'] = int(m.group(4))

      part['bbox'] = (part['vp_width'], part['vp_height'])

    m = dimpat.search(body)
    if m:
      part['bbox2'] = (int(m.group(1)), int(m.group(2)))

    m = defpat.search(body)
    if m:
      defs = m.group(1)
      defs = defs.replace("glyph", "glyph%d_" % n)
      part['defs'] = defs
    else:
      logging.debug("no def in %s" % fn)

    m = drawpat.search(body)
    if m:
      draw = m.group(1)
      part['draw'] = draw.replace("glyph", "glyph%d_" % n)

    logging.debug(prefix + ": %s (%d %d %d %d)" % (part['bbox'], part['vp_minx'], part['vp_miny'], part['vp_width'], part['vp_height']))

  return parts

def layoutParts(parts, viewport_size, margin=2, outermargin=10):
  #packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline, rotation=True)
  packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline, rotation=False)

  for n,part in enumerate(parts):
    rid = packer.add_rect(part['bbox'][0]+margin, part['bbox'][1]+margin, n)

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
      part['x'] = rect.x+margin//2
      part['y'] = rect.y+margin//2

      rratio = rect.width / rect.height
      pratio = part['bbox'][0] / part['bbox'][1]

      dr = abs(rratio - pratio)

      if dr > 0.1:
        part['rotated'] = True
  return pages

def writeSVG(outfn, parts, viewport_size, outermargin=10, units="mm"):
  minx = 12000
  miny = 12000
  vp_max_width = 0
  vp_max_height = 0
  dimx = 0
  dimy = 0

  for n,part in enumerate(parts):
    minx = min(minx, part['x'])
    miny = min(miny, part['y'])

    dimx += part['bbox'][0]
    dimy = max(dimy, part['bbox'][1])

    vp_max_width = max(vp_max_width, part['vp_width'])
    vp_max_height = max(vp_max_height, part['vp_height'])

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
  fp.write('  viewBox="%d %d %d %d"\n' % (minx-outermargin, miny+outermargin, viewport_size[0], viewport_size[1]))
  fp.write('  version="1.1">\n')

  fp.write('<sodipodi:namedview id="namedview312" inkscape:document-units="%s" />\n' % units)

  fp.write("<defs>\n")
  for part in parts:
    if 'defs' in part:
      fp.write(part['defs'])
  fp.write("</defs>\n")

##  for r in range(0,90+15, 30):
  if 1:
    r = 90
    for n,part in enumerate(parts):
      if 'draw' in part:
        fp.write('<g transform="')
        if part['rotated']: fp.write('rotate(%d %d %d) ' % (r, 
                                                            part['vp_minx'], 
                                                            part['vp_miny']))
        fp.write('translate(%d %d) ' % (part['x'], -part['y']))
        fp.write('">\n')
        fp.write(part['draw'])
        fp.write('</g>\n')

  fp.write("</svg>\n")

  fp.close()

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
    writeSVG(fn, _parts, viewport_size, outermargin, units)

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
