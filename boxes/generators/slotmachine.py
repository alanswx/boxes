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


    def drawfront(self, move=None):
        t = self.thickness

        if self.move(self.width+self.margin, self.front+self.margin, move, True): return

        flexheight=15

        self.moveTo(0, 0)

        self.edges["F"](self.width)
        self.corner(90)
        self.edges["f"](self.front)
        #self.corner(90)
        self.edges["X"](flexheight,self.width)
        self.edges["f"](self.fronttop-flexheight)
        self.corner(90)
        self.edges["F"](self.width)
        self.corner(90)
        self.edges["f"](self.fronttop-flexheight)
        self.edges["e"](flexheight)
        self.edges["f"](self.front)

        self.move(self.width+self.margin, self.front+self.margin, move)

    def side(self, move=None):
        if self.move(self.depth+self.margin, self.backwall+self.margin, move, True): return

        self.moveTo(0, 0)

        self.edges["F"](self.depth)
        self.corner(90)
        self.edges["F"](self.backwall)
        self.corner(90)
        self.edges["f"](self.topdepth)
        self.corner(60)
        self.edges["F"](self.fronttop)
        self.corner(30)
        self.edges["F"](self.front)

        self.move(self.depth+self.margin, self.backwall+self.margin, move)

        return
        
    def render(self):
        self.thickness = 3.1
        self.burn = .25
        self.reference = 0.0

        self.width =  365.0
        self.height = 457.0
        self.depth =  330.0
        self.margin = 5.0

        self.backwall = self.height
        self.topdepth = self.depth * .75
        dx = (self.depth - self.topdepth)
        self.fronttop = dx / math.cos(math.radians(60))
        self.front = self.height - (dx / math.tan(math.radians(30)))


        # Initialize canvas
        self.open()
       
        t = self.thickness

        self.ctx.set_font_size(30)

        self.text("floor", self.width/2, self.depth/2, align="center")
        #self.rectangularWall(self.width, self.depth - t*2, "fFfF", move="right")
        self.rectangularWall(self.width, self.depth-t*2, "fFfF", move="right")

        self.text("front", self.width/2, self.front/2, align="center")
        self.drawfront(move="right")

        self.text("top", self.width/2, self.topdepth/2, align="center")
        self.rectangularWall(self.width, self.topdepth, "fFfF", move="right")

        self.text("left side", self.depth/2, self.backwall/2, align="center")
        self.side(move="right")

        self.text("right side", self.depth/2, self.backwall/2, align="center")
        self.side(move="right")

        # f's: bottom, right,top,left 
        self.text("back", self.width/2, self.backwall/2, align="center")
        self.rectangularWall(self.width, self.backwall, "FfFf", move="right")

        self.close()

