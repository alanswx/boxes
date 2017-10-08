#!/usr/bin/env python3
# Copyright (C) 2017  Alan Steremberg
# Copyright (C) 2013-2016 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *

class SlotMachine(Boxes):
    """Desktop SlotMachine"""
    
    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.argparser.add_argument(
            "--width",  action="store", type=float, default=355.0,
            help="inner width of the console")

    def side(self, move=None):
        # TODO: Add callbacks

        y, h = self.y, self.h
        t = self.thickness

        if self.move(y+35, h+155, move, True):
            return

        self.moveTo(10, 0)
        self.edges["f"](y)
        self.polyline(1, (90, 1))
        self.edges["f"](h)
        self.polyline(1, (90, 1))
        self.edges["f"](self.topdepth)
        self.polyline(1, (60, 1))
        self.edges["f"](self.fronttop)
        self.polyline(1, (30, 1))
        self.edges["f"](self.front)
        self.polyline(1, (90, 1))
        #self.edges["f"](h)
        #self.polyline(1, (90, 10))
        self.move(y+10, h+30, move)

        return
        self.moveTo(45, 0)
        self.fingerHolesAt(10, 10, self.bottom, 0)
        self.polyline(y-30, (90, 10))
        self.fingerHolesAt(0.5*t, 10, self.back, 0)
        self.fingerHolesAt(h-40-40, 10, self.back, 0)
        
        self.polyline(h-10, (45, 10))
        self.fingerHolesAt(0, 10, self.topback, 0)
        self.fingerHolesAt(200, 10+0.5*t, self.top, 90)
        self.fingerHolesAt(200-0.5*t, 110, self.speaker, -180)
        self.polyline(200, (90, 10), 100, (90, 10), 100, (-90, 10),  350, (-30, 10))
        self.fingerHolesAt(0, 10, self.keyb, 0)
        self.fingerHolesAt(-0.5*t, 10+0.5*t, self.keyback, 90)
        self.fingerHolesAt(150+0.5*t, 10+0.5*t, self.front, 90)
        self.polyline(150, (90, 10), 124.45, (75, 10), 5)

        self.move(y+35, h+155, move)
        
    def render(self):
        y, h = self.y, self.h = 330, 457
        width = self.width
        t = self.thickness

        self.bottom = y-0.5*t
        self.backwall = h
        self.front = 304
        self.fronttop = 176
        self.topdepth = 241

        

        # Initialize canvas
        self.open()
        # Floor AJS
        self.rectangularWall(width, self.bottom, "efff", move="up")
        # Back
        self.rectangularWall(width, self.backwall, move="up")

        # Front bottom
        self.rectangularWall(width, self.front, "efff", move="up")
        # Front Top
        self.rectangularWall(width, self.fronttop, "efff", move="up")

        # Sides
        self.side(move="up")
        self.side(move="up")

        self.close()

