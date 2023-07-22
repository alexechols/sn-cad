import numpy as np
from vector import *

class PrimitiveGeomObject:
    def __init__(self, scale = 1, pos = Vector3(0, 0, 0), rotor = Quaternion(0, 0, 0, 1), parent = None):
        """
        Generic base class for storing information about geometry objects. 
        Largely to be subclassed for specific primative types, provides a parent type for common information.

        scale : int | float | list[int] | list[float] | Vector3 = 1
            Specifies the scale of each primary axis of the object (before rotation).
            If scale is an int or float, each axis is scaled by that amount.
            If scale is a list, x, y, and z axes are scaled by respective amounts given in list.

        pos : list[int] | list[float] | Vector3 = Vector3(0, 0, 0)
            Specifies the relative position of self to the origin of the parent object.
            Recursively applies up the object tree.

        rotor : Quaternion = Quaternion(0, 0, 0, 1)
            Quaternion rotor describing the orientation of the geometry in 3D space.
            Axis of rotor is the axis that stays constant, angle is about that axis

        parent : None | GeomObject = None
            GeomObject parent of self.
        """

        #Pos type checking and initialization
        if not isinstance(pos, (Vector3, list[int], list[float])):
            raise ValueError("pos must be a Vector3 or a length 3 list of numeric types")
        
        if isinstance(pos, list) and len(pos) != 3:
            raise ValueError("pos must be a Vector3 or a length 3 list of numeric types")
        
        if isinstance(pos, Vector3):
            self.pos = pos
        else:
            self.pos = Vector3(*pos)

        #Scale type checking and initialization
        if not isinstance(scale, (int, float, list[int], list[float], Vector3)):
            raise ValueError("scale must be numeric, a length 3 list of numeric types, or a Vector3")
        
        if isinstance(scale, (int, float)):
            self.scale = Vector3(scale, scale, scale)
        
        elif isinstance(scale, Vector3):
            self.scale = scale

        else:
            if len(scale) != 3:
                raise ValueError("scale must be numeric, a length 3 list of numeric types, or a Vector3")

            self.scale = Vector3(*scale)

        #Orientaion type checking and initialization
        if not isinstance(rotor, Quaternion):
            raise ValueError("rotation_axis must be a Quaternion")
        
        self.rotor = rotor

        #Parent type checking and initialization
        if not isinstance(parent, (None, GeomObject)):
            raise ValueError("parent must be None or a GeomObject")
        
        self.parent = parent

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        
        return self
    
    def get_pos(self):
        if self.parent:
            return self.pos + self.parent.get_pos()

        return self.pos

    def get_orientation(self):
        if self.parent:
            rotor_queue = []

            parent = self

            while parent.parent:
                rotor_queue.append(parent.rotor)
            
            out_rotor = rotor_queue[-1]
            for rotor in rotor_queue[:-1]:
                out_rotor = rotor * out_rotor

            return out_rotor
        
        return self.rotor


class GeomObject:
    pass