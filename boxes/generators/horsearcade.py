#!/usr/bin/env python3

import boxes
from boxes import *


class HorseArcade(Boxes):
    """Fully closed box"""

    ui_group = "HorseArcade"

    def __init__(self):
      Boxes.__init__(self)
      self.addSettingsArgs(edges.FingerJointSettings)
      self.buildArgParser("outside")

    def label(self, text, x=0, y=0, angle=0, align=""):
      if not self.show_labels: return
      self.text(text, x, y, angle=angle, align=align)

    def drawBoxOpening(self,x):
      with self.ctx:
        self.cointray_width=150
        self.cointray_height=50
        cx = x+self.cointray_width/2
        self.moveTo(cx - self.cointray_width/2, 20)

        self.edges['e'](self.cointray_width)
        self.corner(90)
        self.edges['e'](self.cointray_height)
        self.corner(90, 20)
        self.edges['e'](self.cointray_width-40)
        self.corner(90, 20)
        self.edges['e'](self.cointray_height)
        self.corner(90)

    def leftStand(self):
      with self.ctx:
        self.label("leftStand", self.width/2, 25, align="center")

        # glass holes
        self.fingerHolesPlastic(self.thickness*1,
                           self.candyHeight+self.corner_dy+self.height + self.thickness,
                           self.tower_height-self.corner_dy-self.height - self.candyHeight, 90)  #left
        self.fingerHolesPlastic(self.thickness*1 + self.candyDepth,
                           self.candyHeight+self.corner_dy+self.height + self.thickness,
                           self.tower_height-self.corner_dy-self.height - self.candyHeight, 90)  ## right

        self.fingerHolesAt(0, self.height+self.thickness-self.thickness/2+self.burn*2, self.depth, 0)

        self.fingerHolesAt(0, self.corner_dy+self.height-self.thickness/2, 
                           self.candyDepth + self.thickness*2, 0)

        self.edges['e'](self.depth)
        self.corner(90)
        self.edges['f'](self.height)
        self.edges['e'](self.thickness)
        self.corner(90)
        self.edges['e'](self.depth - self.corner_dx - self.tower_depth)
        self.corner(-math.degrees(self.corner_angle_radians))
        self.edges['e'](self.corner_length)
        self.corner(-math.degrees(self.corner_angle_radians))
        self.edges['e'](self.tower_height-self.corner_dy-self.height)
        self.corner(90)
        self.edges['e'](self.tower_depth)
        self.corner(90)
        self.edges['e'](self.tower_height-self.height)
        self.edges['e'](self.thickness)
        self.edges['f'](self.height)

    def rightStand(self):
      with self.ctx:
        self.label("rightStand", (self.corner_dx+self.tower_depth)/2, 25, align="center")
        # glass holes
        self.fingerHolesPlastic(self.thickness*1, 
                                self.candyHeight+self.corner_dy+self.thickness*0, 
                                self.tower_height-self.corner_dy-self.height - self.candyHeight, 90)
        self.fingerHolesPlastic(self.thickness*1+self.candyDepth, 
                                self.candyHeight+self.corner_dy+self.thickness*0, 
                                self.tower_height-self.corner_dy-self.height - self.candyHeight, 90)

        #self.fingerHolesAt(0, self.corner_dy-self.thickness/2, self.tower_depth, 0)
        self.fingerHolesAt(0, self.corner_dy-self.thickness/2-self.thickness, 
                           self.candyDepth + self.thickness*2, 0)

        self.edges['f'](self.corner_dx+self.tower_depth)
        self.corner(180)
        self.corner(-math.degrees(self.corner_angle_radians))
        self.edges['e'](self.corner_length)
        self.corner(-math.degrees(self.corner_angle_radians))
        self.edges['e'](self.tower_height-self.corner_dy-self.height)
        self.corner(90)
        self.edges['e'](self.tower_depth)
        self.corner(90)
        self.edges['e'](self.tower_height-self.height)


    def pusherTray(self):
      with self.ctx:
        self.edges['e'](self.candyWidth)
        self.corner(90)
        self.edges['f'](self.candyDepth)
        self.edges['e'](self.thickness*1)
        self.corner(-90)
        self.edges['e'](self.bracketWidth)
        self.corner(90)
        self.edges['e'](self.bracketDepth)
        self.corner(90)
        self.edges['e'](self.bracketWidth+self.candyWidth)
        self.corner(90)
        self.edges['f'](self.bracketDepth)
        self.edges['e'](self.thickness*1)
        self.edges['f'](self.candyDepth)

        self.hole(self.candyWidth/2+self.bracketWidth, self.bracketDepth+self.candyDepth/2, 2.5/2)
        self.hole(-(self.bracketDepth+self.candyDepth-15), self.candyWidth+self.bracketWidth/2, 5)
        self.hole(-(self.bracketDepth+self.candyDepth-15-47), self.candyWidth+self.bracketWidth/2, 5)

    def render(self):
      self.show_labels = False
      #self.show_labels = True

      self.thickness = 5.0
      self.plasticThickness = 2.50
      self.burn = .30
      edges.FingerJointSettings.play = .300
      self.reference = 0.0

      boxes.defaultStrokeColor = boxes.RED
      boxes.holeStrokeColor = boxes.RED

      self.open()

      self.width = 400
      self.depth = 300
      self.height = 100

      self.candyWidth=55
      self.candyDepth=94
      self.candyHeight=12
      self.bracketWidth=22
      self.bracketDepth=82

      self.buttonHoleDiameter = 25


      if self.outside:
        self.width = self.adjustSize(self.width)
        self.depth = self.adjustSize(self.depth)
        self.height = self.adjustSize(self.height)

      s = edges.FingerJointSettings(self.plasticThickness, relative=False, 
                                    space=10, finger=10,
                                    width=self.plasticThickness)
      self.addPart(edges.FingerHoles(self, s), name="fingerHolesPlastic")

      self.corner_dy = self.height
      self.corner_dx = self.height

      self.corner_length = math.sqrt(self.corner_dx*self.corner_dx+self.corner_dy*self.corner_dy)
      self.corner_angle_radians = math.atan(self.corner_dy/self.corner_dx)

      self.tower_depth = self.candyDepth + self.thickness * 2
      self.tower_height = self.height + self.corner_dy + self.candyHeight * 50

      self.leftStand()
      self.moveTo(self.corner_dx + self.tower_depth*2, 0)

      self.rightStand()
      self.moveTo(self.tower_depth *2, 0)

      with self.ctx:
        self.rectangularWall(self.width, self.height, "eFFF")
        self.moveTo(0, self.height + self.thickness*2)

        self.rectangularWall(self.depth, self.height, "efFf")
        self.moveTo(0, self.height + self.thickness*2)

        self.rectangularWall(self.width, self.height, "eFFF")
        self.moveTo(0, self.height + self.thickness*2)

        ## top
        if 1:
          #self.rectangularHole(130/2+25,150/2+y/2,130,150)
          offset = (self.candyWidth + self.thickness*2)
          areaWidth = self.width - offset - self.thickness*1

          self.hole(offset + areaWidth/4, self.depth/4, self.buttonHoleDiameter/2)  ## button 1
          self.hole(offset + 3*(areaWidth/4), self.depth/4, self.buttonHoleDiameter/2)      ## button 2

          self.fingerHolesAt(self.candyWidth + self.thickness*2, 
                             self.tower_depth - self.thickness*3, 
                             self.corner_dx+self.tower_depth, 90)

          self.rectangularWall(self.width, self.depth, "ffff")

        self.moveTo(0, self.depth + self.thickness*4)

        self.pusherTray()
        self.moveTo(self.bracketDepth * 2, self.bracketDepth)

        self.rectangularWall(self.bracketDepth, self.thickness*2, "Feee")

      # bottom
      self.moveTo(self.width + self.thickness*4, 0)

      # plastic
      self.rectangularWall(self.candyWidth, 
                           self.tower_height-self.corner_dy-self.height - self.candyHeight, "efef")
      self.moveTo(self.candyWidth*2, 0)

      self.rectangularWall(self.candyWidth, 
                           self.tower_height-self.corner_dy-self.height - self.candyHeight, "efef")

      self.close()
