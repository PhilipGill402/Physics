import numpy as np

class Object:
    def __init__(self, x:int, y:int, velocity:np.array, mass:float, restitution:float, color:tuple):
        self.x = x
        self.y = y 
        self.velocity = velocity
        self.mass = mass
        self.restitution = restitution
        self.color = color
        if self.mass == 0:
            self.invMass = 0
        else:
            self.invMass = 1 / self.mass

        
        def velocityVerlet(position, acceleration, dt):
            pass