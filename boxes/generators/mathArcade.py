#!/usr/bin/env python3

import boxes
from boxes import *


class MathArcade(Boxes):
    """Fully closed box"""

    ui_group = "MathArcade"

    def __init__(self):
      Boxes.__init__(self)
      self.addSettingsArgs(edges.FingerJointSettings)
      self.buildArgParser("outside")

    def label(self, text, x=0, y=0, angle=0, align=""):
      if not self.show_labels: return
      self.ctx.set_source_rgb(*self.etchStrokeColor)
      self.text(text, x, y, angle=angle, align=align)
      self.ctx.set_source_rgb(*boxes.defaultStrokeColor)

    def dispenserStand(self):
      with self.ctx:

        # glass holes
        if 0:
          self.fingerHolesPlastic(self.thickness*1,
                           self.candyHeight+self.corner_dy+self.dispenserHeight + self.thickness,
                           self.towerHeight-self.corner_dy-self.dispenserHeight - self.candyHeight, 90)  #left
        self.fingerHolesPlastic(self.thickness*1 + self.candyDepth,
                           self.candyHeight+self.corner_dy+self.dispenserHeight + self.thickness,
                           self.towerHeight-self.corner_dy-self.dispenserHeight - self.candyHeight, 90)  ## right

        self.fingerHolesAt(0, self.dispenserHeight+self.thickness-self.thickness/2+self.burn*2, 
                           self.dispenserDepth, 0)
        self.fingerHolesAt(0, self.corner_dy+self.dispenserHeight-self.thickness/2, 
                           self.candyDepth + self.thickness*2, 0)

        self.edges['e'](self.dispenserDepth)
        self.corner(90)
        self.edges['f'](self.dispenserHeight)
        self.edges['e'](self.thickness)
        self.corner(90)
        self.edges['e'](self.dispenserDepth - self.corner_dx - self.towerDepth)
        self.corner(-math.degrees(self.corner_angle_radians))
        self.edges['e'](self.corner_length)
        self.corner(-math.degrees(self.corner_angle_radians))
        self.edges['e'](self.towerHeight-self.corner_dy-self.dispenserHeight)
        self.corner(90)
        self.edges['e'](self.towerDepth)
        self.corner(90)
        
        self.edges['e'](self.towerHeight-self.dispenserHeight)
        self.edges['e'](self.thickness)
        self.edges['f'](self.dispenserHeight)

    def rightStand(self):
      with self.ctx:
        self.label("rightStand", (self.corner_dx+self.towerDepth)/2, 25, align="center")
        # glass holes
        self.fingerHolesPlastic(self.thickness*1, 
                                self.candyHeight+self.corner_dy+self.thickness*0, 
                                self.towerHeight-self.corner_dy-self.dispenserHeight - self.candyHeight, 90)
        self.fingerHolesPlastic(self.thickness*1+self.candyDepth, 
                                self.candyHeight+self.corner_dy+self.thickness*0, 
                                self.towerHeight-self.corner_dy-self.dispenserHeight - self.candyHeight, 90)

        #self.fingerHolesAt(0, self.corner_dy-self.thickness/2, self.towerDepth, 0)
        self.fingerHolesAt(0, self.corner_dy-self.thickness/2-self.thickness, 
                           self.candyDepth + self.thickness*2, 0)

        self.edges['f'](self.corner_dx+self.towerDepth)
        self.corner(180)
        self.corner(-math.degrees(self.corner_angle_radians))
        self.edges['e'](self.corner_length)
        self.corner(-math.degrees(self.corner_angle_radians))
        self.edges['e'](self.towerHeight-self.corner_dy-self.dispenserHeight)
        self.corner(90)
        self.edges['e'](self.towerDepth)
        self.corner(90)
        self.edges['e'](self.towerHeight-self.dispenserHeight)

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

      self.etchStrokeColor = boxes.BLUE
      self.cutStrokeColor = boxes.RED

      boxes.defaultStrokeColor = self.cutStrokeColor
      boxes.holeStrokeColor = self.cutStrokeColor

      self.ajoiningBoltDiameter = 5

      self.candyWidth=58
      self.candyDepth=96
      self.candyHeight=12

      self.dispenserWidth = self.candyWidth
      self.dispenserDepth = 200
      self.dispenserHeight = 50

      self.bracketWidth=22
      self.bracketDepth=82

      self.corner_dy = self.dispenserHeight
      self.corner_dx = self.dispenserHeight

      self.corner_length = math.sqrt(self.corner_dx*self.corner_dx+self.corner_dy*self.corner_dy)
      self.corner_angle_radians = math.atan(self.corner_dy/self.corner_dx)

      self.towerCandyCapacity = 30
      self.towerDepth = self.candyDepth + self.thickness * 2
      self.towerHeight = self.dispenserHeight + self.corner_dy + self.candyHeight * self.towerCandyCapacity

      ## console dimensions

      self.buttonDiameter = 50
      self.buttonHoleDiameter = 30

      self.consoleWidth = self.buttonDiameter*2 + self.buttonDiameter
      self.consoleDepth = self.dispenserDepth
      self.consoleHeight = 50

      s = edges.FingerJointSettings(self.plasticThickness, relative=False, 
                                    space=10, finger=10,
                                    width=self.plasticThickness)
      self.addPart(edges.FingerHoles(self, s), name="fingerHolesPlastic")

      ## button console
      with self.groupctx() as m:
        self.label("Console", self.consoleWidth/2, 25, align="center")
        self.label("Front", self.consoleWidth/2, 15, align="center")
        self.rectangularWall(self.consoleWidth, self.consoleHeight, "eFFF")

      with self.groupctx() as m:
        self.label("Console", self.consoleWidth/2, 25, align="center")
        self.label("Rear", self.consoleWidth/2, 15, align="center")
        self.rectangularWall(self.consoleWidth, self.consoleHeight, "eFFF")

      ## top
      with self.groupctx() as m:
        self.label("Console", self.consoleWidth/2, 25, align="center")
        self.label("Top", self.consoleWidth/2, 15, align="center")

        self.rectangularWall(self.consoleWidth, self.consoleDepth, "ffff")
        self.moveTo(self.thickness, self.thickness)
        # button 1
        self.hole(self.consoleWidth/3, self.consoleDepth/3, self.buttonHoleDiameter/2)  
        # button 2
        self.hole(2*(self.consoleWidth/3), self.consoleDepth/3, self.buttonHoleDiameter/2)

        # button 3
        self.hole(self.consoleWidth/3, 2*self.consoleDepth/3, self.buttonHoleDiameter/2)  
        # button 4
        self.hole(2*(self.consoleWidth/3), 2*self.consoleDepth/3, self.buttonHoleDiameter/2)

      with self.groupctx() as m:
        self.label("Console", self.consoleDepth/2, 25, align="center")
        self.label("Right Side", self.consoleDepth/2, 15, align="center")
        self.rectangularWall(self.consoleDepth, self.consoleHeight, "efFf")

        if 1:
          ## ajoining holes
          self.hole(self.ajoiningBoltDiameter*3 + 2*self.thickness, 
                    self.ajoiningBoltDiameter*2 + 2*self.thickness,
                    self.ajoiningBoltDiameter/2)

          self.hole(self.consoleDepth+(2*self.thickness) - (self.ajoiningBoltDiameter*3 + 2*self.thickness), 
                    self.ajoiningBoltDiameter*2 + 2*self.thickness,
                    self.ajoiningBoltDiameter/2)

      with self.groupctx() as m:
        self.label("Console", self.consoleDepth/2, 25, align="center")
        self.label("Left Side", self.consoleDepth/2, 15, align="center")
        self.rectangularWall(self.consoleDepth, self.consoleHeight, "efFf")

        if 1:
          ## ajoining holes
          self.hole(self.ajoiningBoltDiameter*3 + 2*self.thickness, 
                    self.ajoiningBoltDiameter*2 + 2*self.thickness,
                    self.ajoiningBoltDiameter/2)

          self.hole(self.consoleDepth+(2*self.thickness) - (self.ajoiningBoltDiameter*3 + 2*self.thickness), 
                    self.ajoiningBoltDiameter*2 + 2*self.thickness,
                    self.ajoiningBoltDiameter/2)


      self.groupClose("box.svg", (1220, 609))
