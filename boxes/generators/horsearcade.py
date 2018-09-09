#!/usr/bin/env python3

import boxes
from boxes import *


class HorseArcade(Boxes):
    """Fully closed box"""

    ui_group = "HorseArcade"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.buildArgParser("x", "y", "h", "outside")
    def label(self, text, x=0, y=0, angle=0, align=""):
      if not self.show_labels: return
      self.text(text, x,y,angle=angle, align=align)

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


    def leftSide(self,move):
            self.ctx.save()


            with self.ctx:
                self.label("leftSide", self.x/2, 25, align="center")

                # glass holes
                self.fingerHolesAt(self.thickness*2,
                                   self.candyHeight+self.corner_dy+self.h-self.thickness/2, 
                                   self.tower_height-self.corner_dy-self.h, 90)  #left
                self.fingerHolesAt(self.thickness*2 + self.candyDepth,
                                   self.candyHeight+self.corner_dy+self.h-self.thickness/2, 
                                   self.tower_height-self.corner_dy-self.h, 90)  ## right

                #self.fingerHolesAt(0, self.h-self.thickness/2, self.corner_dx+self.tower_depth, 0)
                self.fingerHolesAt(0, self.h+self.thickness-self.thickness/2+self.burn*2, self.y, 0)
                #self.fingerHolesAt(0, self.corner_dy+self.h-self.thickness/2, self.tower_depth, 0)
                self.fingerHolesAt(0, self.corner_dy+self.h-self.thickness/2, self.candyDepth + self.thickness*2, 0)

                self.edges['e'](self.y)
                self.corner(90)
                self.edges['f'](self.h)
                self.edges['e'](self.thickness)
                self.corner(90)
                self.edges['e'](self.y - self.corner_dx - self.tower_depth)
                self.corner(-math.degrees(self.corner_angle_radians))
                self.edges['e'](self.corner_length)
                self.corner(-math.degrees(self.corner_angle_radians))
                self.edges['e'](self.tower_height-self.corner_dy-self.h)
                self.corner(90)
                self.edges['e'](self.tower_depth)
                self.corner(90)
                self.edges['e'](self.tower_height-self.h)
                self.edges['e'](self.thickness)
                self.edges['f'](self.h)

            #self.move(self.y+self.thickness, self.tower_height, move)
            self.move(self.corner_dx + self.tower_depth + self.thickness, self.h+self.thickness, move)

    def rightStand(self,move):
            self.ctx.save()

            with self.ctx:
                self.label("rightStand", (self.corner_dx+self.tower_depth)/2, 25, align="center")
                # glass holes
                self.fingerHolesAt(self.thickness*2, 
                                   self.candyHeight+self.corner_dy-self.thickness/2, 
                                   self.tower_height-self.corner_dy-self.h, 90)
                self.fingerHolesAt(self.thickness*2+self.candyDepth, 
                                   self.candyHeight+self.corner_dy-self.thickness/2, 
                                   self.tower_height-self.corner_dy-self.h, 90)

                self.fingerHolesAt(0, self.corner_dy-self.thickness/2, self.tower_depth, 0)

                self.edges['f'](self.corner_dx+self.tower_depth)
                self.corner(180)
                self.corner(-math.degrees(self.corner_angle_radians))
                self.edges['e'](self.corner_length)
                self.corner(-math.degrees(self.corner_angle_radians))
                self.edges['e'](self.tower_height-self.corner_dy-self.h)
                self.corner(90)
                self.edges['e'](self.tower_depth)
                self.corner(90)
                self.edges['e'](self.tower_height-self.h)
            self.move(self.corner_dx+self.tower_depth+self.thickness, self.h, move)


    def pusherTray(self,move):
            self.ctx.save()

            with self.ctx:
                self.edges['e'](self.candyWidth)
                self.corner(90)
                self.edges['f'](self.candyDepth)
                self.corner(-90)
                self.edges['e'](self.bracketWidth)
                self.corner(90)
                self.edges['e'](self.bracketDepth)
                self.corner(90)
                self.edges['e'](self.bracketWidth+self.candyWidth)
                self.corner(90)
                self.edges['e'](self.bracketDepth)
                self.edges['f'](self.candyDepth)

                self.hole(self.candyWidth/2+self.bracketWidth, self.bracketDepth+self.candyDepth/2, 2.5/2)
                self.hole(-(self.bracketDepth+self.candyDepth-15), self.candyWidth+self.bracketWidth/2, 5)
                self.hole(-(self.bracketDepth+self.candyDepth-15-47), self.candyWidth+self.bracketWidth/2, 5)

            self.move(self.candyWidth+self.bracketWidth+self.thickness*2, self.h, move)



    def render(self):
        #self.show_labels = False
        self.show_labels = True
        self.thickness = 5.0
        self.burn = .30
        self.reference = 0.0

        boxes.defaultStrokeColor = boxes.RED
        boxes.holeStrokeColor = boxes.RED

        self.open()
        #x = 500
        x = 400
        y = 300
        h = 100
        #x, y, h = self.x, self.y, self.h

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            h = self.adjustSize(h)

        t = self.thickness
        self.x=x
        self.y=y
        self.h=h
        self.corner_dy = self.h
        self.corner_dx = self.h
        self.corner_length = math.sqrt(self.corner_dx*self.corner_dx+self.corner_dy*self.corner_dy)
        self.corner_angle_radians = math.atan(self.corner_dy/self.corner_dx)

        self.candyWidth=55
        self.candyDepth=91
        self.candyHeight=12
        self.bracketWidth=22
        self.bracketDepth=82

        self.tower_depth = self.candyDepth + self.thickness * 4
        self.tower_height = self.h + self.corner_dy + self.candyHeight * 50

        d2 = edges.Bolts(2)
        d3 = edges.Bolts(3)

        d2 = d3 = None
        with self.ctx:
          self.leftSide(move=None)
          
        self.moveTo(self.corner_dx + self.tower_depth*2, 0)

        with self.ctx:
          self.rightStand(move=None)

        self.moveTo(self.tower_depth *2, 0)

        with self.ctx:
          #self.drawBoxOpening(25)
          self.rectangularWall(x, h, "eFFF", bedBolts=[d2] * 4, move=None)

        self.moveTo(0, h + self.thickness*2)

        with self.ctx:
          self.rectangularWall(y, h, "efFf", bedBolts=[d3, d2, d3, d2], move=None)

          #self.rectangularWall(y, h, "efFf", bedBolts=[d3, d2, d3, d2], move="up")
          #self.rectangularWall(y, h, "efFf", bedBolts=[d3, d2, d3, d2],move="up")

        self.moveTo(0, h + self.thickness*2)

        with self.ctx:
          self.rectangularWall(x, h, "eFFF", bedBolts=[d2] *4, move=None)

        self.moveTo(0, h + self.thickness*2)

        ## top
        with self.ctx:
          #self.rectangularHole(130/2+25,150/2+y/2,130,150)
          self.hole(self.x-100-150, y/4, 24/2)  ## button 1
          self.hole(self.x-100, y/4, 24/2)      ## button 2
          self.fingerHolesAt(self.candyWidth + self.thickness*2, self.tower_depth - self.thickness*2, 
                             self.corner_dx+self.tower_depth, 90)

          self.rectangularWall(x, y, "ffff", bedBolts=[d2, d3, d2, d3], move=None)

        self.moveTo(0, y + self.thickness*4)

        with self.ctx:
          self.pusherTray(move="right up")

        # bottom
        
        #self.rectangularWall(x, y, "ffff", bedBolts=[d2, d3, d2, d3])

        if 0:
          # plastic
          self.rectangularWall(self.candyWidth, self.tower_height-self.corner_dy-self.h, "efef", bedBolts=[d2] *4, move="right")
          self.rectangularWall(self.candyWidth, self.tower_height-self.corner_dy-self.h, "efef", bedBolts=[d2] *4, move="right")

        self.close()
