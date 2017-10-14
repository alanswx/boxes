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

    def draw_front(self, move=None):
        t = self.thickness
        
        with self.movectx(self.width+self.margin*2, self.front+self.margin, move) as m:
          if m:
            self.moveTo(0, -self.thickness)

            with self.ctx:
              # bottom
              self.edges["F"](self.width-t*2)

              # right
              self.corner(90)
              self.edges["f"](self.front-self.flexheight/2)
              self.edges["X"](self.flexheight,self.width-t*2)
              self.edges["f"](self.topdepth-self.flexheight/2)

              # top
              self.corner(90)
              self.edges["e"](self.width-t*2)

              # left
              self.corner(90)
              self.edges["f"](self.topdepth-self.flexheight/2)
              self.edges["e"](self.flexheight)
              self.edges["f"](self.front-self.flexheight/2)

            ## screen

            with self.ctx:
              cx = self.width/2
              cy = self.front + self.fronttop/2
              self.moveTo(cx - self.screen_width/2, cy - self.screen_height/2)
              self.draw_rect(self.screen_width, self.screen_height)

            ## tray
            with self.ctx:
              cx = self.width/2
              cy = self.front + self.fronttop/2
              self.moveTo(cx - self.cointray_width/2, 20)
              
              self.edges['e'](self.cointray_width)
              self.corner(90)
              self.edges['e'](self.cointray_height)
              self.corner(90, 20)
              self.edges['e'](self.cointray_width-40)
              self.corner(90, 20)
              self.edges['e'](self.cointray_height)
              self.corner(90)
              
              #self.roundedPlate(self.cointray_width, self.cointray_height, 20, edge="e")
              #self.rectangularWall(self.cointray_width, self.cointray_height, "eeee")

    def draw_side(self, move=None):
      with self.movectx(self.depth+self.margin*2, self.height+self.margin, move) as m:
        if m:
          cd = 0
          d = 1

          self.continueDirection(math.radians(0))
          with self.ctx:
            self.moveTo(0, 0)

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
          with self.ctx:
            self.moveTo((self.thickness*2+30), self.tray_elevation)
            self.continueDirection(math.radians(0))
            self.edges["h"](self.tray_depth, no_continue=True)


    @restore
    def draw_servo(self, x,y,move=None):
      self.moveTo(x,y)
      w = 20
      h = 40
      self.draw_rect(w, h)

      self.hole(w/2+5, -5, 2.5/2)
      self.hole(w/2-5, -5, 2.5/2)
      self.hole(w/2+5, h+5, 2.5/2)
      self.hole(w/2-5, h+5, 2.5/2)


    def draw_chute(self, move=None):
      with self.movectx(self.chute_width+self.margin*2, self.chute_length, move) as m:
        if m:
          self.rectangularWall(self.chute_width-self.thickness, self.chute_length-self.thickness, "efef", move=None)      

    def draw_chute_side(self, move=None):
      with self.movectx(self.depth+self.margin*2, self.tray_elevation, move) as m:
        if m:
          #self.rectangularWall(self.chute_side_width, self.tray_elevation-self.thickness, "feee", move=None)      
          # we need to notch out a spot for the servo - so no simple rectangle
          sides="feee"
          self.edges[sides[0]](self.chute_side_width)
          self.corner(90)
          self.edges[sides[1]](self.tray_elevation-self.thickness)
          self.corner(90)
          self.edges[sides[2]](self.chute_side_width-100)
          self.corner(90)
          self.edges[sides[2]](40)
          self.corner(-90)
          self.edges[sides[2]](100)
          self.corner(90)
          self.edges[sides[3]](self.tray_elevation-self.thickness-40)
          self.corner(90)
          ## coin tray floor holes
          with self.ctx:
            self.moveTo(self.thickness*0, 20)
            self.continueDirection(math.radians(0))
            self.edges["h"](self.cointray_depth, no_continue=True)

          ## chute holes
          with self.ctx:
            self.moveTo((self.thickness*0+60), 20)
            self.continueDirection(self.chute_angle_radians)
            self.edges["h"](self.chute_length, no_continue=True)

    def draw_cointray(self, move=None):
      with self.movectx(self.chute_width+self.margin*2, self.cointray_depth, move) as m:
        if m:
          self.edges['e'](self.cointray_width-40)
          self.corner(90, 20)
          self.edges['e'](self.cointray_height)
          self.edges['f'](self.cointray_depth-self.thickness)
          self.corner(90)          
          self.edges['e'](self.cointray_width)
          self.corner(90)
          self.edges['f'](self.cointray_depth-self.thickness)
          self.edges['e'](self.cointray_height)
          self.corner(90, 20)
          
          #self.rectangularWall(self.chute_width, self.cointray_depth-self.thickness, "efef", move=None)      

    def draw_cointray_buildup(self,move=None):
      with self.movectx(self.chute_width+self.margin*2, self.cointray_depth, move) as m:
        if m:
          # bottom edge (minus 40 for round 20 sides)
          self.edges['e'](self.cointray_width-40)
          self.corner(90, 20)
          # side
          self.edges['e'](self.cointray_height)
          self.corner(90)          
          # back small part
          self.edges['e'](20)
          self.corner(90)          
          self.edges['e'](self.cointray_height-20)
          self.corner(-90,20)          
          self.edges['e'](self.cointray_width-80)
          self.corner(-90,20)          
          self.edges['e'](self.cointray_height-20)
          self.corner(90)          
          self.edges['e'](20)
          self.corner(90)
          self.edges['e'](self.cointray_height)
          self.corner(90, 20)
          
          #self.rectangularWall(self.chute_width, self.cointray_depth-self.thickness, "efef", move=None)      

    def draw_tray(self, move=None):
      with self.movectx(self.tray_width+self.margin*2, self.tray_depth, move) as m:
        if m:
          with self.ctx:
            self.moveTo(0, 0)
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

          with self.ctx:
            self.moveTo(cx-self.raceway_width-self.raceway_width/2, 0)

            self.draw_servo(self.raceway_width+5, 10)
            self.moveTo(0, 40+20)

            self.draw_rect(self.raceway_width, self.raceway_height)

            self.moveTo(-10, self.raceway_height)
            self.draw_rect(self.raceway_width+20, 70)

          with self.ctx:
            self.moveTo(cx+self.raceway_width/2, 0)

            self.draw_servo(self.raceway_width+5, 10)
            self.moveTo(0, 40+20)

            self.draw_rect(self.raceway_width, self.raceway_height)

            self.moveTo(-10, self.raceway_height)
            self.draw_rect(self.raceway_width+20, 70)


    def hatch_backing(self, move=None):
      with self.movectx(self.hatch_width+self.margin*2, self.hatch_height, move) as m:
        if m:
          cx = (self.hatch_width+20)/2
          cy = (self.hatch_height+20)/2

          with self.ctx:
            self.moveTo(cx - (self.hatch_width+20)/2, cy-(self.hatch_height+20)/2)
            self.draw_rect(self.hatch_width+20, self.hatch_height+20)

          with self.ctx:
            self.moveTo(cx - (self.hatch_width-40)/2, cy-(self.hatch_height-40)/2)
            self.roundedPlate(self.hatch_width-40, self.hatch_height-40, 20, edge="e")

    @restore
    def draw_cross(self, cx, cy, width):
      for angle in (0,90,180,270):
        with self.ctx:
          self.moveTo(cx, cy)
          self.continueDirection(math.radians(angle))
          self.edges['e'](width)
      
    def draw_pusher(self,move=None):
      #self.pusher_width
      #self.pusher_depth
      with self.movectx(self.pusher_width+self.margin*2, self.pusher_depth, move) as m:
        if m:
          with self.ctx:
            self.edges['e'](self.pusher_depth)
            self.corner(90)
            self.edges['e'](self.pusher_width)
            self.corner(90)
            self.edges['e'](self.pusher_depth)
            self.corner(180)
            a = math.pi/2
            n = 10 
            da =  math.pi / n
            with self.ctx:
              r=self.pusher_width/2
              for i in range(n):
                self.ctx.arc_negative(0, -r, r, a,a-da)
                a -= da
          self.moveTo(self.pusher_depth+self.thickness*2,self.pusher_width/2+self.thickness)
          self.continueDirection(math.radians(180))
          self.edges['h'](self.pusher_tab_width,no_continue=True)

    def draw_pusher_tab(self,move=None):
      with self.movectx(self.pusher_tab_width, self.pusher_tab_width, move) as m:
        if m:
          self.rectangularWall(self.pusher_tab_width, self.pusher_tab_width, "eefe", move=None, exterior=True)
          self.hole(self.pusher_tab_width/2,self.pusher_tab_width/2,1.5)

    @restore
    def draw_rect(self, width, height, sides='eeee'):
      self.edges[sides[0]](width)
      self.corner(90)
      self.edges[sides[1]](height)
      self.corner(90)
      self.edges[sides[2]](width)
      self.corner(90)
      self.edges[sides[3]](height)
      self.corner(90)

    def draw_floor(self, move=None):
      with self.movectx(self.width, self.depth, move) as m:
        if m:
          self.rectangularWall(self.width, self.depth, "ffff", move=None, exterior=True)

          ## chute holes
          with self.ctx:
            self.moveTo((self.width/2 - self.chute_width/2)+self.thickness, (self.thickness*1+self.burn*4))
            self.continueDirection(math.radians(90))
            self.edges["h"](self.chute_side_width, no_continue=True)

          ## chute holes
          with self.ctx:
            self.moveTo((self.width/2 + self.chute_width/2)+self.thickness*2, (self.thickness*1+self.burn*4))
            self.continueDirection(math.radians(90))
            self.edges["h"](self.chute_side_width, no_continue=True)
          

    def draw_back(self, move=None):
      with self.movectx(self.width+self.margin*2, self.height+self.margin*2, move) as m:
        if m:
          self.moveTo(self.margin, 0)

          with self.ctx:
            self.rectangularWall(self.width-self.thickness*2, self.height-self.thickness, "FfFf", move=None)
            #self.draw_rect(self.width-self.thickness*2, self.height-self.thickness*0, "FfFf")

            ## draw hatch
            cx = self.width/2
            cy = self.height/2
            self.moveTo(cx - self.hatch_width/2, cy-self.hatch_height/2)
            self.roundedPlate(self.hatch_width, self.hatch_height, 20, edge="e")

          ## draw tray holes
          self.moveTo(self.thickness*1, self.height/2-20+self.thickness)
          self.continueDirection(math.radians(0))
          dx = cx - self.hatch_width/2

          self.edges["h"](dx-self.thickness*1, no_continue=True)
          self.moveTo(self.hatch_width+dx-self.thickness*1, 0)
          self.edges["h"](dx, no_continue=True)
        
    def label(self, text, x=0, y=0, angle=0, align=""):
      if not self.show_labels: return
      self.text(text, x,y,angle=angle, align=align)

    def render(self):
        self.thickness = 2.8
        self.thickness = 5.0
        self.burn = .30
        self.reference = 0.0

        self.show_labels = False

        ## exterior dimensions
        self.width =  365.0
        self.height = 530.0
        self.depth =  335.0
        self.margin = 10.0
        self.flexheight=20

        self.cointray_width = 150
        self.cointray_height = 50
        self.cointray_depth = 60

        indepth = self.depth-self.thickness*0
        self.topdepth = indepth * .658
        dx = (indepth - self.topdepth)
        self.fronttop = dx / math.cos(math.radians(60))
        self.front = (self.height-self.thickness*1) - (dx / math.tan(math.radians(30)))

        self.hatch_width = self.width * .80
        self.hatch_height = self.height * .80

        self.tray_depth = self.depth - 30 - self.thickness*2
        self.tray_width = self.width - self.thickness*2
        self.tray_elevation = self.height/2-20

        self.chute_side_width = self.depth*.85

        self.chute_elevation = 20+self.thickness*1
        self.chute_width = self.cointray_width+self.thickness*1
        dy = self.tray_elevation-self.chute_elevation
        dx = self.depth - self.cointray_depth - self.thickness*2
        self.chute_length = math.sqrt(dx*dx+dy*dy)
        self.chute_angle_radians = math.atan(dy/dx)
        #self.chute_length = math.sin(math.radians(self.chute_angle)) * dy*2


        self.raceway_width = 40
        self.raceway_height = 134

        self.dispenser_width = 43.5

        self.screen_width = 218
        self.screen_height = 137
        self.screen_inner_width = 230
        self.screen_inner_height = 151

        self.pusher_width=39+self.burn*2
        self.pusher_depth=90
        self.pusher_tab_width=10*self.thickness

        for key in ("width", "height", "depth", "topdepth", "flexheight",
                    "fronttop", "front", "burn", "thickness", "margin"):
          print ("%10s: %6.2f mm" % (key, getattr(self, key)))

        #edges.FingerJointSettings.surroundingspaces = 1.0

        # Initialize canvas
        self.open()
        self.ctx.set_source_rgb(1,0,0)
       
        t = self.thickness

        self.ctx.set_font_size(30)

        with self.ctx:
          self.moveTo(0, self.depth+self.margin+self.thickness)

          self.label("left side", self.depth/2, self.height/2, align="center")
          self.draw_side(move=None)

        self.moveTo(self.depth+self.margin, 0)

        with self.ctx:
          self.label("floor", self.width/2, self.depth/2, align="center")
          self.draw_floor(move="up")

          self.moveTo(self.thickness, self.margin)

          self.label("front", self.width/2, self.front/2, align="center")
          self.draw_front(move="up")

          self.moveTo(0, self.front+self.margin)

          self.label("top", self.width/2, self.topdepth/2, align="center")
          self.rectangularWall(self.width, self.topdepth, "eFfF", exterior=True)
          cx = self.width/2
          cy = self.topdepth/2

          ## dispenser tube holes
          thy = self.topdepth - (self.tray_depth - (15+40+10+self.raceway_height)) - self.dispenser_width/2
          self.hole(cx - self.raceway_width + self.thickness/2, thy, self.dispenser_width/2 - self.burn)
          self.hole(cx + self.raceway_width + self.thickness/2, thy, self.dispenser_width/2 - self.burn)

        self.moveTo(self.width, 0)

        with self.ctx:
          self.moveTo(self.margin, self.depth+self.margin)
          self.label("right side", self.depth/2, self.height/2, align="center")
          self.draw_side(move=None)

          cx = self.depth/2
          cy = self.height/2
          self.hole(cx, 60, 54/2)

        self.moveTo(self.depth+self.margin*2, 0)

        with self.ctx:
          # back
          self.moveTo(0, self.depth+self.margin-self.thickness)
          self.label("back", self.width/2, self.height/2, align="center")
          self.draw_back(move="up")

          ## draw hatch backing
          self.label("hatch backing", self.hatch_width/2, self.hatch_height/2, align="center")
          self.hatch_backing(move="right")

        self.moveTo(self.width+self.margin*2, 0)

        with self.ctx:
          self.label("tray", self.tray_width/2, self.tray_depth/2, align="center")
          self.draw_tray(move="up")

          self.moveTo(0, self.margin*2)

          self.label("chute", self.chute_width/2, self.chute_length/2, align="center")
          self.draw_chute(move="up")

          self.moveTo(0, self.margin*2)
          with self.ctx:
            self.label("chute tray", self.chute_width/2, self.cointray_depth/2, align="center")
            self.draw_cointray(move="right")

            num_buildup = math.ceil(20 / self.thickness)
            for i in range(num_buildup):
                self.label("chute tray buildup", self.chute_width/2, self.cointray_depth/2, align="center")
                self.draw_cointray_buildup(move="right")

          self.moveTo(0, self.margin*1+self.pusher_depth)
          self.draw_pusher(move="up")

          self.moveTo(0, self.margin*1+self.pusher_depth)
          self.draw_pusher_tab(move="up")

          self.moveTo(0, self.margin*1+self.cointray_depth)
          self.draw_chute_side(move="up")

          self.moveTo(0, self.margin*1)
          self.draw_chute_side(move="up")

        self.moveTo(self.tray_width+self.margin*2, 0)

        with self.ctx:
          w = self.width-self.thickness*2
          h = self.topdepth - self.thickness*2
          self.draw_rect(w, h)
          self.moveTo(w/2-self.screen_inner_width/2 + self.thickness, 
                      h/2-self.screen_inner_height/2)
          self.draw_rect(self.screen_inner_width, self.screen_inner_height)

        self.close()

