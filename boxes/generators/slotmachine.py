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
            "--width",  action="store", type=float, default=365.0,
            help="inner width of the console")

        self.y = 330
        self.h = 457
        self.width = 365.0
        
        self.bottom = self.y - 2*self.thickness
        self.backwall = self.h
        self.front = 305
        self.fronttop = 176
        self.topdepth = 241

    def drawfront(self, move=None):
        t,y,h,width = (self.thickness, self.y, self.h, self.width)

        if self.move(y+35, h+155, move, True):
            return

        flexheight=15

        self.moveTo(0, 0)
        self.edges["f"](width)
        self.corner(90)
        self.edges["F"](self.front-flexheight)
        #self.corner(90)
        self.edges["X"](flexheight,width)
        self.edges["F"](self.fronttop)
        self.corner(90)
        self.edges["f"](width)
        self.corner(90)
        self.edges["F"](self.fronttop)
        self.edges["e"](flexheight)
        self.edges["F"](self.front-flexheight)
        self.move(y+10, h+30, move)

    def side(self, move=None):
        t,y,h,width = (self.thickness, self.y, self.h, self.width)

        if self.move(y+35, h+155, move, True):
            return

        self.moveTo(10, 0)
        self.edges["F"](y)
        self.corner(90)
        self.edges["F"](self.backwall)
        self.corner(90)
        self.edges["F"](self.topdepth)
        self.corner(60)
        self.edges["F"](self.fronttop)
        self.corner(30)
        self.edges["F"](self.front)
        self.move(y+10, h+30, move)

        return
        
    def render(self):
        t,y,h,width = (self.thickness, self.y, self.h, self.width)

        # Initialize canvas
        self.open()
       
        # Floor AJS
        self.rectangularWall(width, self.bottom, "fFfF", move="up")
        # Back
        # f's: bottom, right,top,left 
        self.rectangularWall(width, self.backwall-2*t, "FfFf", move="up")
        #top 
        self.rectangularWall(width, self.topdepth-2*t, "ffff", move="up")

        self.drawfront(move="up")
        
        # Sides
        self.side(move="up")
        self.side(move="up")

        self.close()

