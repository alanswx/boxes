#!/usr/bin/env python3

import boxes
from boxes import *


class HorseArcade2(Boxes):
    """Fully closed box"""

    ui_group = "HorseArcade2"

    def __init__(self):
      Boxes.__init__(self)
      self.addSettingsArgs(edges.FingerJointSettings)
      self.addSettingsArgs(edges.HingeSettings)

      self.buildArgParser("outside")

    def label(self, text, x=0, y=0, angle=0, align=""):
      if not self.show_labels: return
      self.ctx.set_source_rgb(*self.etchStrokeColor)
      size = self.text(text, x, y, angle=angle, align=align)
      self.ctx.set_source_rgb(*boxes.defaultStrokeColor)
      return size

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
        if 0:
          self.fingerHolesAt(0, self.corner_dy+self.dispenserHeight-self.thickness/2,
                             self.candyDepth + self.thickness*2, 0)

        self.edges['e'](self.dispenserDepth)
        self.corner(90)
        self.edges['f'](self.dispenserHeight)
        self.edges['e'](self.thickness)
        self.corner(90)
        if 0:
          self.edges['e'](self.dispenserDepth - self.corner_dx - self.towerDepth)
          self.corner(-math.degrees(self.corner_angle_radians))
          self.edges['e'](self.corner_length)
          self.corner(-math.degrees(self.corner_angle_radians))
        else:
          self.edges['e'](self.dispenserDepth - self.corner_dx - self.towerDepth)
          self.corner(-90)

        self.edges['e'](self.towerHeight-self.corner_dy-self.dispenserHeight)
        self.corner(90)
        self.edges['f'](self.towerDepth)
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
        self.rectangularHole(self.thickness*1, (self.dispenserDepth + self.gearHeight/2) + self.thickness*2, self.gearDepth, 65)

        ## connection to the servo side wall
        self.fingerHolesAt(22,
                           self.dispenserDepth + self.thickness - self.burn,
                           self.bracketDepth - self.thickness, 90)

        self.edges['f'](self.candyWidth)
        self.corner(90)
        self.edges['f'](self.dispenserDepth)

        self.edges['f'](self.bracketDepth)
        self.corner(90)
        self.edges['e'](self.candyWidth)
        self.corner(90)
        self.edges['f'](self.bracketDepth)

        self.edges['f'](self.dispenserDepth)

        self.ctx.stroke()      

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
      self.ctx.stroke()

    def render(self):
      self.show_labels = False
      #self.show_labels = True

      self.thickness = 5.00
      self.plasticThickness = 2.50
      self.burn = .20
      edges.FingerJointSettings.play = .3
      self.reference = 0.0

      #edges.HingeSettings.style = "outset"
      #edges.HingeSettings.pinwidth = .9
      #edges.HingeSettings.grip_percentage = .5
      #edges.HingeSettings.grip_length = 5*2
      #edges.HingeSettings.axle = .5
      #edges.HingeSettings.hingestrength = 3

      self.etchStrokeColor = boxes.BLUE
      self.cutStrokeColor = boxes.RED

      boxes.defaultStrokeColor = self.cutStrokeColor
      boxes.holeStrokeColor = self.cutStrokeColor

      #self.ajoiningBoltDiameter = 5
      self.ajoiningBoltDiameter=6.75

      self.gearDepth = 10
      self.gearHeight = 68

      self.servoWidth = 40.5
      self.servoHeight = 20
      self.servoDepth = 40
      self.servoArm = 11

      self.candyWidth=54
      self.candyDepth=96
      self.candyHeight=12

      self.dispenserWidth = self.candyWidth
      self.dispenserDepth = 200
      self.dispenserHeight = 70

      self.pusherHeight = 12

      self.bracketWidth=22
      self.bracketDepth=self.candyDepth

      self.corner_dy = 0
      self.corner_dx = 0

      if 0:
        self.corner_dy = self.dispenserHeight
        self.corner_dx = self.dispenserHeight
        self.corner_length = math.sqrt(self.corner_dx*self.corner_dx+self.corner_dy*self.corner_dy)
        self.corner_angle_radians = math.atan(self.corner_dy/self.corner_dx)
        
        
      self.towerCandyCapacity = 30
      self.towerDepth = self.candyDepth + self.thickness * 2
      self.towerHeight = self.dispenserHeight + self.corner_dy + self.candyHeight * self.towerCandyCapacity

      ## console dimensions

      self.buttonDiameter = 100
      self.buttonHoleDiameter = 25

      self.consoleWidth = self.buttonDiameter*2 + self.buttonDiameter
      self.consoleDepth = self.dispenserDepth
      self.consoleHeight = 70


      with self.groupctx() as m:
        s = edges.FingerJointSettings(self.plasticThickness, relative=False,
                                      space=10, finger=10,
                                      width=self.plasticThickness)
        self.addPart(edges.FingerHoles(self, s), name="fingerHolesPlastic")

        self.label("Dispenser", self.dispenserDepth/2, 25, align="center")
        self.label("Left Stand", self.dispenserDepth/2, 15, align="center")
        self.dispenserStand()
        if 1:
          ## holes for the door bracket
          self.fingerHolesAt(1, self.candyHeight+self.corner_dy+self.dispenserHeight + self.thickness + 3,
                             self.candyDepth + self.thickness*2, 0)
        if 1:
          ## ajoining holes
          self.hole(self.ajoiningBoltDiameter*3 + 2*self.thickness,
                    self.ajoiningBoltDiameter*2 + 2*self.thickness,
                    self.ajoiningBoltDiameter/2)

          self.hole(self.dispenserDepth+(2*self.thickness) - (self.ajoiningBoltDiameter*3 + 2*self.thickness),
                    self.ajoiningBoltDiameter*2 + 2*self.thickness,
                    self.ajoiningBoltDiameter/2)

      with self.groupctx() as m:
        s = edges.FingerJointSettings(self.plasticThickness, relative=False,
                                      space=10, finger=10,
                                      width=self.plasticThickness)
        self.addPart(edges.FingerHoles(self, s), name="fingerHolesPlastic")

        self.label("Dispenser", self.dispenserDepth/2, 25, align="center")
        self.label("Right Stand", self.dispenserDepth/2, 15, align="center")
        self.dispenserStand()
        if 1:
          ## ajoining holes
          self.hole(self.ajoiningBoltDiameter*3 + 2*self.thickness,
                    self.ajoiningBoltDiameter*2 + 2*self.thickness,
                    self.ajoiningBoltDiameter/2)

          self.hole(self.dispenserDepth+(2*self.thickness) - (self.ajoiningBoltDiameter*3 + 2*self.thickness),
                    self.ajoiningBoltDiameter*2 + 2*self.thickness,
                    self.ajoiningBoltDiameter/2)

      with self.groupctx() as m:
        self.label("Dispenser", self.dispenserWidth/2, 25, align="center")
        self.label("rear", self.dispenserWidth/2, 15, align="center")
        self.rectangularWall(self.dispenserWidth, self.dispenserHeight, "eFeF")
        ## connection to Servo side wall
        self.fingerHolesAt(22 + 7,
                           0,
                           self.dispenserHeight, 90)

      with self.groupctx() as m:
        self.label("Dispenser", self.dispenserWidth/2, 25, align="center")
        self.label("front", self.dispenserWidth/2, 15, align="center")
        self.rectangularWall(self.dispenserWidth, self.dispenserHeight, "eFFF")
        self.moveTo(0, self.dispenserHeight + self.thickness*2)

        ## top
        if 0:
          self.label("Dispenser", self.dispenserWidth/2, 25, align="center")
          self.label("top", self.dispenserWidth/2, 15, align="center")
          self.rectangularWall(self.dispenserWidth, self.dispenserDepth, "ffff")

      with self.groupctx() as m:
        self.label("Servo side wall", self.bracketDepth/2, 10, align="center")
        w,h = self.rectangularWall(self.bracketDepth - self.thickness - self.burn, self.dispenserHeight,  "eeff")

        with self.ctx:
          #self.moveTo(h/2 - self.servoHeight/2, h - self.servoWidth/2 - 15 - 1)
          self.moveTo(self.servoWidth/2 + 32 - self.thickness, h - self.servoWidth/2 - 15 - 1)
          self.moveTo(0,0,90)
          #self.rectangularHole(0, 0, self.servoWidth, self.servoHeight)
          with self.ctx:
            self.moveTo(-self.servoWidth/2, -self.servoHeight/2)
            self.draw_rect(self.servoWidth, self.servoHeight)
          self.hole(-self.servoWidth/2-4, -self.servoHeight/2+2+3, 2)
          self.hole(-self.servoWidth/2-4, -self.servoHeight/2+2+13, 2)
          self.hole(self.servoWidth/2+4, -self.servoHeight/2+2+3, 2)
          self.hole(self.servoWidth/2+4, -self.servoHeight/2+2+13, 2)

      if 0:
        with self.groupctx() as m:
          self.label("Servo side wall", self.bracketDepth/2, 10, align="center")
          ret = self.rectangularWall(self.servoHeight + self.gearHeight/2, self.dispenserHeight,  "eefe")
          with self.ctx:
            self.moveTo(h/2 - self.servoHeight/2, h - self.servoWidth/2 - 15)
            self.moveTo(0,0,90)
            self.rectangularHole(0, 0, self.servoWidth, self.servoHeight)

      with self.groupctx() as m:
        self.label("Pusher top wall", self.bracketDepth/2, 10, align="center")
        self.rectangularWall(self.candyWidth, self.bracketDepth, "efef")

      with self.groupctx() as m:
        self.label("Pusher side wall", self.bracketDepth/2, 10, align="center")
        self.rectangularWall(self.bracketDepth, self.pusherHeight, "FeFe")

      with self.groupctx() as m:
        self.label("Pusher side wall", self.bracketDepth/2, 10, align="center")
        self.rectangularWall(self.bracketDepth, self.pusherHeight, "FeFe")

      with self.groupctx() as m:
        profile_shift = 0
        pressure_angle = 30
        modulus = 7.7
        teeth2 = 25
        mh = 5.6

        self.gears(teeth=teeth2, dimension=modulus, angle=pressure_angle, spoke_count=0,
                   mount_hole=mh, profile_shift=profile_shift, move=None)


      with self.groupctx() as m:
        self.label("pusherTray", self.candyWidth/2, 25, align="center")
        self.pusherTray()

      with self.groupctx() as m:
        # plastic
        self.label("Dispenser", self.candyWidth/2, 25, align="center")
        self.label("front plastic", self.candyWidth/2, 15, align="center")

        self.rectangularWall(self.candyWidth,
                             self.towerHeight-self.corner_dy-self.dispenserHeight-self.candyHeight,
                             "efef")

      if 0:
        with self.groupctx() as m:
          # we don't need the back piece of plastic
          self.label("Dispenser", self.candyWidth/2, 25, align="center")
          self.label("right side", self.candyWidth/2, 15, align="center")
          self.rectangularWall(self.candyWidth,
                               self.towerHeight-self.corner_dy-self.dispenserHeight-self.candyHeight,
                               "efef")

      with self.groupctx() as m:
        self.label("Dispenser", self.candyWidth/2, 25, align="center")
        self.label("back door", self.candyWidth/2, 15, align="center")
        self.rectangularWall(self.candyWidth+self.thickness*5,
                             self.towerHeight-self.corner_dy-self.dispenserHeight-self.candyHeight-self.thickness - self.burn,
                             "IEJe")

      with self.groupctx() as m:
        self.label("Dispenser", self.candyWidth/2, 25, align="center")
        self.label("tube top2", self.candyWidth/2, 15, align="center")
        with self.ctx:
          self.edges['i'](self.candyWidth+self.thickness*6)
          self.corner(90)
          self.edges['e'](self.thickness)
          self.edges['F'](self.towerDepth-self.thickness)
          self.corner(90)
          self.edges['e'](self.candyWidth+self.thickness*2)
          self.corner(90)
          self.edges['F'](self.towerDepth-self.thickness)
          self.corner(-90)
          self.edges['e'](self.thickness*5)
          self.corner(90)
          self.edges['e'](self.thickness*2)

      ## bottom hinge bracket
      with self.groupctx() as m:
        self.label("Door", self.candyWidth/2, 25, align="center")
        self.label("bottom bracket", self.candyWidth/2, 15, align="center")
        with self.ctx:
            self.edges['i'](self.thickness*4)
            self.corner(90)
            self.edges['e'](self.thickness)
            self.edges['f'](self.towerDepth-self.thickness)
            self.corner(90)
            self.edges['e'](self.thickness*2)
            self.corner(90)
            self.edges['e'](self.towerDepth-self.thickness)
            self.corner(-90)
            self.edges['e'](self.thickness*3)
            self.corner(90)
            self.edges['e'](self.thickness*2)
            self.ctx.stroke()      

      ## button console
      with self.groupctx() as m:
        self.label("Console", self.consoleWidth/2, 25, align="center")
        self.label("Front", self.consoleWidth/2, 15, align="center")
        self.rectangularWall(self.consoleWidth, self.consoleHeight, "eFFF")

      with self.groupctx() as m:
        self.label("Console", self.consoleWidth/2, 25, align="center")
        self.label("Rear", self.consoleWidth/2, 15, align="center")
        self.rectangularWall(self.consoleWidth, self.consoleHeight, "eFFF")
        # hole for the ethernet jack
        self.rectangularHole(self.consoleWidth/2, self.consoleHeight/2, 26, 19)

      ## top
      with self.groupctx() as m:
        self.label("Console", self.consoleWidth/2, 25, align="center")
        self.label("Top", self.consoleWidth/2, 15, align="center")

        self.rectangularWall(self.consoleWidth, self.consoleDepth, "ffff")
        self.moveTo(self.thickness, self.thickness)
        # button 1
        self.hole(self.consoleWidth/4, self.consoleDepth/2, self.buttonHoleDiameter/2)
        # holes for small buttons
        # distance: 6.2
        # hole diameter: 3.75
        self.tinybuttonhole=5.5
        self.tinyholedistance=6.1
        self.hole(self.consoleWidth/4-self.buttonHoleDiameter/2-self.tinyholedistance, self.consoleDepth/2, self.tinybuttonhole/2)
        self.hole(self.consoleWidth/4+self.buttonHoleDiameter/2+self.tinyholedistance, self.consoleDepth/2, self.tinybuttonhole/2)

        # button 2
        self.hole(3*(self.consoleWidth/4), self.consoleDepth/2, self.buttonHoleDiameter/2)
        # holes for small buttons
        # distance: 6.2
        # hole diameter: 3.75
        self.hole(3*self.consoleWidth/4-self.buttonHoleDiameter/2-self.tinyholedistance, self.consoleDepth/2, self.tinybuttonhole/2)
        self.hole(3*self.consoleWidth/4+self.buttonHoleDiameter/2+self.tinyholedistance, self.consoleDepth/2, self.tinybuttonhole/2)

        if 0:
          t = boxes.holeStrokeColor
          boxes.holeStrokeColor = self.etchStrokeColor
          self.hole(self.consoleWidth/4, self.consoleDepth/2, self.buttonDiameter/2)
          self.hole(3*(self.consoleWidth/4), self.consoleDepth/2, self.buttonDiameter/2)

          boxes.holeStrokeColor = t

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

      #
      #  raspberry pi box
      #
      with self.groupctx() as m:
        self.piWidth = 150
        self.piDepth = 125
        self.piHeight = 75
        self.label("Pi", self.piWidth/2, 25, align="center")
        self.label("Front", self.piWidth/2, 15, align="center")
        self.rectangularWall(self.piWidth, self.piHeight, "eFFF")

      with self.groupctx() as m:
        self.label("Pi", self.piWidth/2, 25, align="center")
        self.label("Rear", self.piWidth/2, 15, align="center")
        self.rectangularWall(self.piWidth, self.piHeight, "eFFF")
        # hole for the ethernet jack
        jackoffset=-10
        self.rectangularHole(self.piWidth/4+jackoffset, self.piHeight/2, 19, 26)
        #self.rectangularHole(self.piWidth/4+jackoffset, self.piHeight/2, 25, 26)
        self.rectangularHole(2*self.piWidth/4+jackoffset, self.piHeight/2, 19, 26)
        #self.rectangularHole(2*self.piWidth/4+jackoffset, self.piHeight/2, 25, 26)
        self.rectangularHole(3*self.piWidth/4+jackoffset, self.piHeight/2, 19, 26)
        self.rectangularHole(4*self.piWidth/4+jackoffset, self.piHeight/2, 19, 26)

       ## top
      with self.groupctx() as m:
        self.label("Pi", self.piWidth/2, 25, align="center")
        self.label("Top", self.piWidth/2, 15, align="center")
        self.rectangularWall(self.piWidth, self.piDepth, "ffff")

      with self.groupctx() as m:
        self.label("Pi", self.piDepth/2, 25, align="center")
        self.label("Right Side", self.piDepth/2, 15, align="center")
        self.rectangularWall(self.piDepth, self.piHeight, "efFf")
        self.rectangularHole(self.piDepth/2+7.5, self.piHeight/2, 30, 20)

      with self.groupctx() as m:
        self.label("Pi", self.piDepth/2, 25, align="center")
        self.label("Left Side", self.piDepth/2, 15, align="center")
        self.rectangularWall(self.piDepth, self.piHeight, "efFf")
        self.rectangularHole(self.piDepth/2+7.5, self.piHeight/2, 30, 20)

      self.groupClose("box.svg", (1220, 609))
