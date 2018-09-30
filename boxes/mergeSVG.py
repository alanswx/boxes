#! /usr/bin/env python3

"""python program to solve the world problems..."""

import os, sys, string, time, logging, argparse
import re
import logging

from . import svgutil

_version = "0.1"

import rectpack

from lxml import etree as et
from lxml import builder

if 1:
  #from scipy.spatial import ConvexHull
  import scipy.spatial
  import numpy as np
  from shapely.geometry import Point, MultiPoint, Polygon, MultiPolygon

svg_ns = 'http://www.w3.org/2000/svg'

class Part:
  def __init__(self):
    self.size = None
    self.scale = None
    self.viewbox = None
    self.bbox = None
    self.rotated = False

    self.tree = None

def circumcircle(points, simplex):
    """Computes the circumcentre and circumradius of a triangle:
    https://en.wikipedia.org/wiki/Circumscribed_circle#Circumcircle_equations
    """
    A = [points[simplex[k]] for k in range(3)]
    M = np.asarray(
        [[1.0] * 4] +
        [[sq_norm(A[k]), A[k][0], A[k][1], 1.0] for k in range(3)],
        dtype=np.float32)
    S = np.array([
      0.5 * np.linalg.det(M[1:, [0, 2, 3]]),
      -0.5 * np.linalg.det(M[1:, [0, 1, 3]])
    ])
    a = np.linalg.det(M[1:, 1:])
    b = np.linalg.det(M[1:, [0, 1, 2]])
    centre, radius = S / a, np.sqrt(b / a + sq_norm(S) / a**2)
    return centre, radius


def get_alpha_complex(alpha, points, simplexes):
    """Obtain the alpha shape.
    Args:
        alpha (float): the paramter for the alpha shape
        points: data points
        simplexes: the list of indices that define 2-simplexes in the Delaunay
            triangulation
    """
    return filter(lambda simplex: circumcircle(points, simplex)[1] < alpha,
                  simplexes)


def concave_hull(points, alpha, delunay_args=None):
    """Computes the concave hull (alpha-shape) of a set of points.
    """
    delunay_args = delunay_args or {
      'furthest_site': False,
      'incremental': False,
      'qhull_options': None
    }
    triangulation = scipy.spatial.Delaunay(np.array(points))
    alpha_complex = get_alpha_complex(alpha, points, triangulation.simplices)
    X, Y = [], []
    for s in triangulation.simplices:
        X.append([points[s[k]][0] for k in [0, 1, 2, 0]])
        Y.append([points[s[k]][1] for k in [0, 1, 2, 0]])
    poly = Polygon(list(zip(X[0], Y[0])))
    for i in range(1, len(X)):
        poly = poly.union(Polygon(list(zip(X[i], Y[i]))))
    return poly     



def convex_hull(points):
  hull = scipy.spatial.ConvexHull(points)
  hpoints = []
##  for idx in hull.vertices:
##    hpoints.append(points[idx])

  for idx in hull.simplices:
    hpoints.append((points[idx[0]],points[idx[1]]))
  return hpoints

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

    paths, attributes = svgpathtools.svg2paths(fn)

    points = []

    path = svgpathtools.concatpaths(paths)

    if 1:
      for _part in path:
        for pt in _part:
          points.append((pt.real, pt.imag))

      poly = Polygon(points)
      part.hull = list(poly.exterior.coords)
          

    if 0:
      fp = open(fn + ".wkt", "w")

      for n, path in enumerate(paths):
        fp.write("POLYGON ((")
        pieces = []
        for _part in path:
          for m,pt in enumerate(_part):
            pieces.append("%.1f %.1f" % (pt.real, pt.imag))
        fp.write("%s" % ', '.join(pieces))
        fp.write("))\n")
      fp.close()

    if 0:
      #part.hull = convex_hull(points)
      hull = concave_hull(points, alpha=0.15)
      part.hull = list(hull.exterior.coords)

    if 0:
      p = Polygon(points)
      p2 = p.simplify(2, preserve_topology=True)

      if p2.__class__ == MultiPolygon:
        for poly in p2:
          part.hull = list(poly.exterior.coords)
      else:
        part.hull = list(p2.exterior.coords)

      hull = concave_hull(part.hull, alpha=.01)
      part.hull = list(hull.exterior.coords)

      

    if 1:
      xlist = [x for (x,y) in points]
      ylist = [y for (x,y) in points]
      xmin = min(xlist)
      xmax = max(xlist)
      ymin = min(ylist)
      ymax = max(ylist)

      part.bounding = (xmin, ymin, xmax, ymax)
      part.bsize = ((part.bounding[2]-part.bounding[0]), (part.bounding[3] - part.bounding[1]))

    print (fn, n, len(points), part.bounding, part.size, part.bsize)
    logging.debug(prefix + ": size:%s viewbox:%s scale:%s" % (part.size, part.viewbox, part.scale))

  return parts

import svgpathtools

def layoutParts(parts, viewport_size, margin=0, outermargin=0):
  #packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline, bin_algo=rectpack.PackingBin.Global, rotation=True)
  packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline, rotation=True)
  #packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline, bin_algo=rectpack.PackingBin.Global, rotation=False)
  #packer = rectpack.newPacker(mode=rectpack.PackingMode.Offline, rotation=False)

  for n,part in enumerate(parts):
    part.bbox = (part.bbox[0]+margin, part.bbox[1]+margin)
    #part.bbox = (part.bsize[0]+margin, part.bsize[1]+margin)
    rid = packer.add_rect(part.bbox[0], part.bbox[1], n)

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

      if dr > 0.01:
        part.rotated = True
      #print ("%s %d %.2f %.2f %.2f %s %s" % (part.rotated, rect.rid, dr, rratio, pratio, rect, part.bbox))
  return pages

def writeSVG(outfn, parts, viewport_size, margin=0, outermargin=0, units="mm"):
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
  bounding_boxes = []

  for n, part in enumerate(parts):
    x1 = viewBox[0]+part.x 
    y1 = viewBox[1]+viewBox[3]-part.y
    x2 = x1 + part.bsize[0]
    y2 = y1 - part.bsize[1]

    if 0:
      bounding_boxes.append(rect(x1,y1,x2,y2))
      bounding_boxes.append(polyline(x1,y1,part.hull))
    
    for el in part.tree.getroot():
      dest_root.append(el)

      cx = viewBox[0]+part.x + part.bbox[0]//2
      cy = viewBox[1]+viewBox[3]-part.y - part.bbox[1]//2
      #crosses.append(cross((cx, cy), 10))

      cx = viewBox[0]+part.x + margin
      cy = viewBox[1]+viewBox[3]-part.y - margin 
      crosses.append(cross((cx, cy), 10))


      if el.tag.endswith("g"):
        if part.rotated:
          rotation = 90
          el.set("transform", 'rotate(%d %d %d) translate(%d %d)' % (rotation, 
                                                                     cx, cy,
                                                                     part.x - part.bbox[0], 
                                                                     -part.y))
        else:
          el.set("transform", 'translate(%d %d)' % (part.x - outermargin*2 - margin*2,
                                                    -(part.y - outermargin*2 - margin*2)))
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

  if 1:
    for _box in bounding_boxes:
      dest_root.append(_box)

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

def rect(x1,y1,x2,y2):
  x1 = int(x1)
  y1 = int(y1)
  x2 = int(x2)
  y2 = int(y2)
  E = builder.ElementMaker(namespace=svg_ns)
  group = E.g()
  group.append(E.line(x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y1), style="stroke:rgb(0,0,255);stroke-width:1"))
  group.append(E.line(x1=str(x2), y1=str(y1), x2=str(x2), y2=str(y2), style="stroke:rgb(0,0,255);stroke-width:1"))
  group.append(E.line(x1=str(x2), y1=str(y2), x2=str(x1), y2=str(y2), style="stroke:rgb(0,0,255);stroke-width:1"))
  group.append(E.line(x1=str(x1), y1=str(y2), x2=str(x1), y2=str(y1), style="stroke:rgb(0,0,255);stroke-width:1"))
  return group

def polyline(x1,y1,points):
  E = builder.ElementMaker(namespace=svg_ns)
  group = E.g()
  lastpt = None
  for pt in points:
    if lastpt is None:
      lastpt = pt
      continue
    group.append(E.line(x1=str(x1+lastpt[0]), y1=str(y1-lastpt[1]), x2=str(x1+pt[0]), y2=str(y1-pt[1]), style="stroke:rgb(0,0,255);stroke-width:1"))
    lastpt = pt
  group.append(E.line(x1=str(x1+lastpt[0]), y1=str(y1-lastpt[1]), x2=str(x1+points[0][0]), y2=str(y1-points[0][1]), style="stroke:rgb(0,0,255);stroke-width:1"))

  return group

def polyline2(x1,y1,lines):
  E = builder.ElementMaker(namespace=svg_ns)
  group = E.g()
  for pt1,pt2 in lines:
    group.append(E.line(x1=str(x1+pt1[0]), y1=str(y1-pt1[1]), x2=str(x1+pt2[0]), y2=str(y1-pt2[1]), style="stroke:rgb(0,0,255);stroke-width:1"))

  return group
  

#def mergeSVG(outfn, viewport_size, files, margin=2, outermargin=5, units="mm"):
def mergeSVG(outfn, viewport_size, files, margin=0, outermargin=0, units="mm"):
  parts = parseSVGs(files)

  pages = layoutParts(parts, viewport_size, margin)

  if len(pages) > 1:
    _fn, _ext = os.path.splitext(outfn)
    outfn = "%s%%d%s" % (_fn, _ext)

  for pagenum,_parts in enumerate(pages):
    try:
      fn = outfn % pagenum
    except TypeError:
      fn = outfn

    logging.warn("writing page %d SVG %s" % (pagenum, fn))
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
