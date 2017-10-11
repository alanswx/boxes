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
from boxes import servos

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
        self.edges["f"](self.front-self.flexheight/2)
        self.edges["X"](self.flexheight,self.width-t*2)
        self.edges["f"](self.fronttop-self.flexheight)
        self.edges["X"](self.flexheight,self.width-t*2)
        self.edges["f"](self.topdepth-self.flexheight/2)

        # top
        self.corner(90)
        self.edges["F"](self.width-t*2)

        # left
        self.corner(90)
        self.edges["f"](self.topdepth-self.flexheight/2)
        self.edges["e"](self.flexheight)
        self.edges["f"](self.fronttop-self.flexheight)
        self.edges["e"](self.flexheight)
        self.edges["f"](self.front-self.flexheight/2)

        self.ctx.restore()
        self.ctx.save()

        cx = self.width/2
        cy = self.topdepth/2 + self.front + self.fronttop
        
        ## dispenser tube holes
        dx = 238.2 - 165.5
        self.circle(cx - dx/2, cy, 43.5/2)
        self.circle(cx + dx/2, cy, 43.5/2)
        
        ## screen
        screen_width = 218
        screen_height = 137

        self.ctx.restore()
        self.ctx.save()
        cx = self.width/2
        cy = self.front + self.fronttop/2
        self.moveTo(cx - screen_width/2, cy - screen_height/2)
        self.rectangularWall(screen_width, screen_height, "eeee")

        ## tray
        self.ctx.restore()

        cx = self.width/2
        cy = self.front + self.fronttop/2
        self.moveTo(cx - self.cointray_width/2, 20)
        self.roundedPlate(self.cointray_width, self.cointray_height, 20, edge="e")
        #self.rectangularWall(self.cointray_width, self.cointray_height, "eeee")

        self.move(self.width+self.margin*2, self.front+self.margin, move)

    def draw_side(self, move=None):
        if self.move(self.depth+self.margin*2, self.height+self.margin, move, True): return

        self.ctx.save()

        self.moveTo(self.margin, 0)

        # bottom
        self.edges["f"](self.depth - self.thickness*0)

        # right
        self.corner(90)
        self.edges["F"](self.height - self.thickness*1)

        # top
        self.corner(90)
        self.edges["f"](self.topdepth - self.flexheight/2)
        self.edges["e"](self.flexheight/2)

        # left
        self.corner(60)
        self.edges["e"](self.flexheight/2)
        self.edges["F"](self.fronttop-self.flexheight)
        self.edges["e"](self.flexheight/2)
        self.corner(30)
        self.edges["e"](self.flexheight/2)
        self.edges["F"](self.front-self.flexheight/2)

        ## tray holes
        self.ctx.restore()
        self.ctx.save()
        self.moveTo(self.thickness*2+30, self.height/2-20)
        self.continueDirection(math.radians(0))
        self.edges["h"](self.tray_depth, no_continue=True)

        ## coin tray floor holes
        self.ctx.restore()
        self.ctx.save()
        
        self.moveTo(self.thickness*4, 20)
        self.continueDirection(math.radians(0))
        self.edges["h"](self.cointray_depth, no_continue=True)

        ## chute holes
        self.ctx.restore()
        self.moveTo(self.thickness*2+60, 20)
        self.continueDirection(math.radians(45))
        dy = (self.height/2-20) - (20)
        self.chute_length = math.sin(math.radians(45)) * dy*2
        self.edges["h"](self.chute_length, no_continue=True)

        self.move(self.depth+self.margin*2, self.height+self.margin, move)
        return

    @restore
    def draw_servo(self, x,y,move=None):
      self.moveTo(x,y)
      w = 20
      h = 40
      self.roundedPlate(w, h, 0, edge="e")

      self.hole(w/2+6, -5 + self.burn*2, 2)
      self.hole(w/2-6, -5 + self.burn*2, 2)
      self.hole(w/2+6, h+5 + self.burn*2, 2)
      self.hole(w/2-6, h+5 + self.burn*2, 2)


    def draw_chute(self, move=None):
      if self.move(self.width+self.margin*2, 0, move, True): return

      self.rectangularWall(self.width-self.thickness, self.chute_length-self.thickness, "efef", move=None)      
      
      self.move(self.width+self.margin*2, 0, move)

    def draw_cointray(self, move=None):
      if self.move(self.cointray_width+self.margin*2, 0, move, True): return

      self.rectangularWall(self.width-self.thickness, self.cointray_depth-self.thickness, "efef", move=None)      
      
      self.move(self.width+self.margin*2, 0, move)


    def draw_tray(self, move=None):
        if self.move(self.tray_width+self.margin*2, 0, move, True): return
        
        self.ctx.save()
        self.moveTo(self.margin, 0)
        self.edges["e"](self.tray_width)
        self.corner(90)
        self.edges["f"](self.tray_depth)
        self.corner(90)
        dx = (self.tray_width - self.hatch_width)/2
        self.edges["f"](dx)
        self.edges["e"](self.hatch_width)
        self.edges["f"](dx)
        self.corner(90)
        self.edges["f"](self.tray_depth)

        cx = self.tray_width / 2
        cy = self.tray_depth / 2

        self.ctx.restore()

        raceway_width = 40
        raceway_height = 134

        self.ctx.save()
        self.moveTo(cx-raceway_width, 20)

        self.draw_servo(raceway_width+5, 0)
        self.moveTo(0, 40+10)
        self.roundedPlate(raceway_width, raceway_height, 0, edge="e")
        self.moveTo(0-self.burn*2, raceway_height)
        self.roundedPlate(42, 42, 0, edge="e")
        self.ctx.restore()

        self.ctx.save()
        self.moveTo(cx+raceway_width, 20)

        self.draw_servo(raceway_width+5, 0)
        self.moveTo(0, 40+10)
        self.roundedPlate(raceway_width, raceway_height, 0, edge="e")
        self.moveTo(0-self.burn*2, raceway_height)
        self.roundedPlate(42, 42, 0, edge="e")

        self.ctx.restore()
        
        self.move(self.tray_width+self.margin*2, 0, move)
      

    def hatch_backing(self, move=None):
        if self.move(self.hatch_width+self.margin*2, 0, move, True): return

        cx = (self.hatch_width+20)/2
        cy = (self.hatch_height+20)/2

        self.ctx.save()
        self.moveTo(cx - (self.hatch_width+20)/2, cy-(self.hatch_height+20)/2)
        self.roundedPlate(self.hatch_width+20, self.hatch_height+20, 20, edge="e")

        self.ctx.restore()
        self.moveTo(cx - (self.hatch_width-40)/2, cy-(self.hatch_height-40)/2)
        self.roundedPlate(self.hatch_width-40, self.hatch_height-40, 20, edge="e")

        self.move(self.hatch_width+self.margin*2, 0, move)

    def draw_rect(self, width, height, sides='eeee'):
      self.ctx.save()
      self.edges[sides[0]](width)
      self.corner(90)
      d = 26
      edges.FingerJointSettings.surroundingspaces = 0
      if sides[1] != 'e': self.edges['e'](self.thickness+self.burn*d)
      self.edges[sides[1]](height-2*(self.thickness + self.burn*d))
      if sides[1] != 'e': self.edges['e'](self.thickness+self.burn*d)
      edges.FingerJointSettings.surroundingspaces = 2
      self.corner(90)
      self.edges[sides[2]](width)
      self.corner(90)
      edges.FingerJointSettings.surroundingspaces = 0
      if sides[3] != 'e': self.edges['e'](self.thickness+self.burn*d)
      self.edges[sides[3]](height-2*(self.thickness + self.burn*d))
      if sides[3] != 'e': self.edges['e'](self.thickness+self.burn*d)
      edges.FingerJointSettings.surroundingspaces = 2
      self.corner(90)
      self.ctx.restore()
      
        
    def draw_back(self, move=None):
        if self.move(self.width+self.margin*2, 0, move, True): return
      
        self.moveTo(self.margin, 0)

        self.ctx.save()
        #self.rectangularWall(self.width-self.thickness, self.height-self.thickness, "FfFf", move=None)
        self.draw_rect(self.width-self.thickness*2, self.height-self.thickness*0, "FfFf")
        
        ## draw hatch
        cx = self.width/2
        cy = self.height/2
        self.moveTo(cx - self.hatch_width/2, cy-self.hatch_height/2)
        self.roundedPlate(self.hatch_width, self.hatch_height, 20, edge="e")

        self.ctx.restore()

        ## draw tray holes
        self.moveTo(self.thickness*1, self.height/2-20)
        self.continueDirection(math.radians(0))
        dx = cx - self.hatch_width/2

        self.edges["h"](dx-self.thickness*1, no_continue=True)
        self.moveTo(self.hatch_width+dx-self.thickness*1, 0)
        self.edges["h"](dx, no_continue=True)
        
        self.move(self.width+self.margin*2, 0, move)

    def render(self):
        self.thickness = 3.1
        self.burn = .40
        self.reference = 0.0

        ## exterior dimensions
        self.width =  365.0
        #self.height = 457.0
        self.height = 480.0
        self.depth =  330.0
        self.margin = 10.0
        self.flexheight=20

        self.cointray_width = 100
        self.cointray_height = 50
        self.cointray_depth = 60

        indepth = self.depth-self.thickness*0
        self.topdepth = indepth * .70
        dx = (indepth - self.topdepth)
        self.fronttop = dx / math.cos(math.radians(60))
        self.front = (self.height-self.thickness*1) - (dx / math.tan(math.radians(30)))

        self.hatch_width = self.width * .80
        self.hatch_height = self.height * .80

        self.tray_depth = self.depth - 30 - self.thickness*2
        self.tray_width = self.width - self.thickness*2

        for key in ("width", "height", "depth", "topdepth", "flexheight",
                    "fronttop", "front", "burn", "thickness", "margin"):
          print ("%10s: %6.2f mm" % (key, getattr(self, key)))

        #edges.FingerJointSettings.surroundingspaces = 1.0

        # Initialize canvas
        self.open()
        self.ctx.set_source_rgb(1,0,0)
       
        t = self.thickness

        self.ctx.set_font_size(30)

        self.text("floor", self.width/2, self.depth/2, align="center")
        self.rectangularWall(self.width, self.depth, "ffff", move="right", exterior=True)

        self.text("front", self.width/2, self.front/2, align="center")
        self.drawfront(move="right")

        if 0:
          self.text("top", self.width/2, self.topdepth/2, align="center")
          self.rectangularWall(self.width, self.topdepth, "fFfF", exterior=True)
          cx = self.width/2
          cy = self.topdepth/2

          ## dispenser tube holes
          dx = 238.2 - 165.5
          self.circle(cx - dx/2, cy, 43.5/2)
          self.circle(cx + dx/2, cy, 43.5/2)
          self.moveTo(self.width, 0)

        self.text("left side", self.depth/2, self.height/2, align="center")
        self.draw_side(move="right")

        self.text("right side", self.depth/2, self.height/2, align="center")
        self.draw_side(move=None)
        cx = self.depth/2
        cy = self.height/2
        self.circle(cx+50, 60, 54/2)
        self.moveTo(self.depth+self.margin, 0)

        # back
        self.text("back", self.width/2, self.height/2, align="center")
        self.draw_back(move="right")
        
        ## draw hatch backing
        self.text("hatch backing", self.hatch_width/2, self.hatch_height/2, align="center")
        self.hatch_backing("right")

        self.text("tray", self.tray_width/2, self.tray_depth/2, align="center")
        self.draw_tray("right")

        self.text("chute", self.width/2, self.chute_length/2, align="center")
        self.draw_chute("right")


        self.text("chute", self.width/2, self.cointray_depth/2, align="center")
        self.draw_cointray("right")

        

        self.close()

