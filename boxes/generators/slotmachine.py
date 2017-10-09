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

    def text(self, text, *args, **kwargs):
      self.ctx.set_source_rgb(0,0,1)
      Boxes.text(self, text, *args, **kwargs)
      self.ctx.set_source_rgb(1,0,0)

    def drawfront(self, move=None):
        t = self.thickness

        if self.move(self.width+self.margin*2, self.front+self.margin, move, True): return

        self.moveTo(self.margin, 0)
        self.ctx.save()

        # bottom
        self.edges["F"](self.width-t*2)

        # right
        self.corner(90)
        edges.FingerJointSettings.surroundingspaces = 0.0
        self.edges["f"](self.front-self.flexheight/2)
        self.edges["X"](self.flexheight,self.width-t*2)
        self.edges["f"](self.fronttop-self.flexheight/2)

        # top
        self.corner(90)
        edges.FingerJointSettings.surroundingspaces = 1.0
        self.edges["F"](self.width-t*2)

        # left
        self.corner(90)
        self.edges["f"](self.fronttop-self.flexheight/2)
        self.edges["e"](self.flexheight)
        self.edges["f"](self.front-self.flexheight/2)

        
        ## screen
        screen_width = 229.5
        screen_height = 150

        self.ctx.restore()
        self.ctx.save()
        cx = self.width/2
        cy = self.front + self.fronttop/2
        self.moveTo(cx - screen_width/2, cy - screen_height/2)
        self.rectangularWall(screen_width, screen_height, "eeee")

        ## tray
        self.ctx.restore()
        tray_width = 100
        tray_height = 50

        cx = self.width/2
        cy = self.front + self.fronttop/2
        self.moveTo(cx - tray_width/2, 20)
        self.rectangularWall(tray_width, tray_height, "eeee")

        self.move(self.width+self.margin*2, self.front+self.margin, move)

    def side(self, move=None):
        if self.move(self.depth+self.margin*2, self.height+self.margin, move, True): return

        self.moveTo(self.margin, 0)

        # bottom
        self.edges["F"](self.depth)

        # right
        self.corner(90)
        self.edges["F"](self.height)

        # top
        self.corner(90)
        self.edges["f"](self.topdepth)

        # right
        edges.FingerJointSettings.surroundingspaces = 0.0
        self.corner(60)
        self.edges["F"](self.fronttop-self.flexheight/2)
        self.edges["e"](self.flexheight/2)
        self.corner(30)
        self.edges["e"](self.flexheight/2)
        self.edges["F"](self.front-self.flexheight/2)
        edges.FingerJointSettings.surroundingspaces = 1.0

        self.move(self.depth+self.margin*2, self.height+self.margin, move)

        return
        
    def render(self):
        self.thickness = 3.1
        self.burn = .25
        self.reference = 0.0

        ## exterior dimensions
        self.width =  365.0
        #self.height = 457.0
        self.height = 480.0
        self.depth =  330.0
        self.margin = 10.0
        self.flexheight=20

        self.topdepth = self.depth * .70
        dx = (self.depth - self.topdepth)
        self.fronttop = dx / math.cos(math.radians(60))
        self.front = self.height - (dx / math.tan(math.radians(30)))


        for key in ("width", "height", "depth", "topdepth", "flexheight",
                    "fronttop", "front", "burn", "thickness", "margin"):
          print ("%10s: %6.2f mm" % (key, getattr(self, key)))

        edges.FingerJointSettings.surroundingspaces = 1.0

        # Initialize canvas
        self.open()
        self.ctx.set_source_rgb(1,0,0)
       
        t = self.thickness

        self.ctx.set_font_size(30)

        self.text("floor", self.width/2, self.depth/2, align="center")
        self.rectangularWall(self.width, self.depth, "fFfF", move="right", exterior=True)

        self.text("front", self.width/2, self.front/2, align="center")
        self.drawfront(move="right")

        self.text("top", self.width/2, self.topdepth/2, align="center")
        self.rectangularWall(self.width, self.topdepth, "fFfF", exterior=True)
        cx = self.width/2
        cy = self.topdepth/2
        self.circle(cx - 50, cy, 30)
        self.circle(cx + 50, cy, 30)
        self.moveTo(self.width, 0)

        self.text("left side", self.depth/2, self.height/2, align="center")
        self.side(move="right")

        self.text("right side", self.depth/2, self.height/2, align="center")
        self.side(move=None)
        cx = self.depth/2
        cy = self.height/2
        self.circle(cx, cy-self.height/4, 20)
        self.moveTo(self.depth, 0)

        # f's: bottom, right,top,left 
        self.ctx.save()
        self.text("back", self.width/2, self.height/2, align="center")
        self.rectangularWall(self.width, self.height, "FfFf", move=None, exterior=True)
        self.ctx.restore()
        
        ## draw hatch
        hatch_width = self.width * .80
        hatch_height = self.height * .80

        cx = self.width/2
        cy = self.height/2
        self.moveTo(cx - hatch_width/2, cy-hatch_height/2)
        self.roundedPlate(hatch_width, hatch_height, 20, edge="e")
        
        ## draw hatch backing
        self.moveTo(self.width+self.margin, 0)

        cx = (hatch_width+20)/2
        cy = (hatch_height+20)/2

        self.text("hatch backing", cx, cy, align="center")

        self.ctx.save()
        self.moveTo(cx - (hatch_width+20)/2, cy-(hatch_height+20)/2)
        self.roundedPlate(hatch_width+20, hatch_height+20, 20, edge="e")

        self.ctx.restore()
        self.moveTo(cx - (hatch_width-40)/2, cy-(hatch_height-40)/2)
        self.roundedPlate(hatch_width-40, hatch_height-40, 20, edge="e")

        self.close()

