import math
import sys

EPS = 2*sys.float_info.epsilon

class Quaternion:
    def __init__(self, x, y, z, s):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or not isinstance(z, (int, float)) or not isinstance(s, (int,float)):
            raise ValueError(f"Cannot define {type(self)} with elements of type(s) {type(x)}, {type(y)}, {type(z)}, and {type(s)}")
        
        self.x = x
        self.y = y
        self.z = z
        self.s = s

    def __eq__(self, other):
        if not isinstance(other, Quaternion):
            return False
        
        return abs(self.x - other.x) < EPS and abs(self.y - other.y) < EPS and abs(self.z - other.z) < EPS and abs(self.s - other.s) < EPS
    
    def __mul__(self, other):
        if not isinstance(other, (int, float, Quaternion)):
            raise ValueError(f"Multiplication is not defined for {type(self)} and object of type {type(other)}")
        
        if isinstance(other, (int, float)):
            return Quaternion(self.x * other, self.y * other, self.z * other, self.s * other)
        
        s = self.s * other.s - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.s * other.x + other.s * self.x + self.y * other.z - other.y * self.z
        y = self.s * other.y + other.s * self.y + self.z * other.x - other.z * self.x
        z = self.s * other.z + other.s * self.z + self.x * other.y - other.x * self.y

        return Quaternion(x, y, z, s)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError(f"Multiplication is not defined for {type(self)} and object of type {type(other)}")
        
        if abs(other) < EPS:
            raise ZeroDivisionError()
    
        return Quaternion(self.x/other, self.y/other, self.z/other, self.s/other)
    
    def __add__(self, other):
        if not isinstance(other, (Quaternion, int, float)):
            raise ValueError(f"Addition is not defined for {type(self)} and object of type {type(other)}")
        
        return Quaternion(self.x + other.x, self.y + other.y, self.z + other.z, self.s + other.s)
    
    def __sub__(self, other):
        if not isinstance(other, (Quaternion, int, float)):
            raise ValueError(f"Subtraction is not defined for {type(self)} and object of type {type(other)}")
        
        if isinstance(other, Quaternion):
            return Quaternion(self.x - other.x, self.y - other.y, self.z - other.z, self.s - other.s)
        
        return Quaternion(self.x - other, self.y - other, self.z - other, self.s - other)
    
    def __neg__(self):
        return Quaternion(-self.x, -self.y, -self.z, -self.s)
    
    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.s ** 2) 
    
    def __str__(self):
        return f"<{self.x}, {self.y}, {self.z}, {self.s}>"
    
    def __repr__(self):
        return f"<{self.x}, {self.y}, {self.z}, {self.s}>"
    
    def is_multiple(self, other):
        if not isinstance(other, Quaternion):
            raise ValueError(f"Quaternion cannot be a multiple of {type(other)}")
        
        if abs(self.x) < EPS and abs(self.y) < EPS and abs(self.z) < EPS and abs(self.s) < EPS:
            return True
        
        if abs(self.x) > EPS:
            ratio = other.x/self.x
        elif abs(self.y) > EPS:
            ratio = other.y/self.y
        elif abs(self.z) > EPS:
            ratio = other.z/self.z
        else:
            ratio = other.s/self.s

        if abs(abs(self.x * ratio) - abs(other.x)) < EPS and abs(abs(self.y * ratio) - abs(other.y)) < EPS and\
              abs(abs(self.z * ratio) - abs(other.z)) < EPS and abs(abs(self.s * ratio) - abs(other.s)):
            return True
        
        return False

    def conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.s)
    
    def inverse(self):
        return self.conjugate()/(self.norm() ** 2)
    
    @staticmethod
    def construct_rotor(axis, theta):
        if not isinstance(axis, Vector3):
            raise ValueError("Axis must be a Vector3!")
        
        return Quaternion(*(axis * math.sin(theta/2)),math.cos(theta/2))
    
    @staticmethod
    def dot(vect_1, vect_2):
        if not isinstance(vect_1, Quaternion) or not isinstance(vect_2, Quaternion):
            raise ValueError(f"Dot product is not defined for {type(vect_1)} and {type(vect_2)}")
        
        return vect_1.x * vect_2.x + vect_1.y * vect_2.y + vect_1.z * vect_2.z + vect_1.s * vect_2.s
    
    @staticmethod
    def lerp(vect_1, vect_2, t):
        if not isinstance(vect_1, (Vector3, int, float)) or not isinstance(vect_2, (Vector3, int, float)):
            raise ValueError(f"Linear Interpolation not defined for objects of type {type(vect_1)} and {type(vect_2)}")
        
        if type(vect_1) != type(vect_2):
            raise ValueError("Linear Interpolation must be performed on objects of the same type")
        
        return (vect_2 - vect_1) * t + vect_1
    
    @staticmethod
    def rev_lerp(vect_1, vect_2, vect_3):
        if not isinstance(vect_1, (Vector3, int, float)) or not isinstance(vect_2, (Vector3, int, float)) or not isinstance(vect_3, (Vector3, int, float)):
            raise ValueError(f"Reverse linear interpolation is not defined for objects of types {type(vect_1)}, {type(vect_2)}, and {type(vect_3)}")
        
        if type(vect_1) != type(vect_2) or type(vect_2) != type(vect_3):
            if not isinstance(vect_1, (int, float)) or not isinstance(vect_2, (int, float)) or not isinstance(vect_3, (int, float)):
                raise ValueError(f"Reverse linear interpolation must be performed on objects of the same type. \n vect_1: {type(vect_1)}, vect_2: {type(vect_2)}, vect_3: {type(vect_3)}")
        
        return (vect_3 - vect_1)/(vect_2 - vect_1)
    
    @staticmethod
    def i():
        return Quaternion(1, 0, 0, 0)
    
    @staticmethod
    def j():
        return Quaternion(0, 1, 0, 0)
    
    @staticmethod
    def k():
        return Quaternion(0, 0, 1, 0)
    
class Vector3(Quaternion):
    def __init__(self, x, y, z):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or not isinstance(z, (int, float)):
            raise ValueError(f"Cannot define {type(self)} with elements of type(s) {type(x)}, {type(y)}, and {type(z)}")
        
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def angle_between(vect_1, vect_2):
        if not isinstance(vect_1, Vector3) or not isinstance(vect_2, Vector3):
            raise ValueError(f"Angle between is not defined for {type(vect_1)} and {type(vect_2)}")
        
        sq_norm = (vect_1.norm() * vect_2.norm())
        if sq_norm == 0:
            raise ValueError(f"At least one of the given vectors has a magnitude of zero! No solution exists")
        
        cos_ang = Vector3.dot(vect_1, vect_2)/sq_norm
        return math.acos(cos_ang)
    
    @staticmethod
    def cross(vect_1, vect_2):
        if not isinstance(vect_1, Vector3) or not isinstance(vect_2, Vector3):
            raise ValueError(f"Cross product is not defined for objects of type {type(vect_1)} and {type(vect_2)}")
        
        return Vector3(vect_1.y * vect_2.z - vect_1.z * vect_2.y, vect_1.z * vect_2.x - vect_1.z * vect_2.z, vect_1.x * vect_2.y - vect_1.y * vect_2.x)
    
    @staticmethod
    def ccw_angle_between(vect_1, vect_2, plane_normal):
        signed_ang = Vector3.signed_angle_between(vect_1, vect_2, plane_normal)

        if signed_ang >= 0:
            return signed_ang
        else:
            return 2*math.pi + signed_ang
        
    @staticmethod
    def signed_angle_between(vect_1, vect_2, plane_normal):
        if not isinstance(vect_1, Vector3) or not isinstance(vect_2, Vector3) or not isinstance(plane_normal, Vector3):
            raise ValueError(f"Angle between is not defined for vectors of type(s) {type(vect_1)} and {type(vect_2)}, and plane normal of type {type(plane_normal)}")
        
        cross = Vector3.cross(vect_1, vect_2)
        if not plane_normal.is_multiple(cross):
            raise ValueError(f"Plane Normal must be a real multiple of the cross product of vect_1 and vect_2")
        
        if plane_normal.norm() < EPS:
            raise ValueError("Normal vector cannot have 0 magnitude!")
        unit_normal = plane_normal/plane_normal.norm()

        signed_ang = math.atan2(Vector3.dot(cross, unit_normal), Vector3.dot(vect_1, vect_2))

        return signed_ang
    
class Vector2(Vector3):
    def __init__(self, x, y):
        super().__init__(x, y, 0)

    @staticmethod
    def signed_cross_mag(vect_1, vect_2):
        if not isinstance(vect_1, Vector3) or not isinstance(vect_2, Vector3):
            raise ValueError(f"Cross product is not defined for objects of type(s) {type(vect_1)} and {type(vect_2)}")

        return Vector3.cross(vect_1, vect_2).z

class Plane:
    def __init__(self, vect_1, vect_2, point):
        if not isinstance(vect_1, Vector3):
            raise ValueError("vect_1 must be a Vector3!")
        
        if not isinstance(vect_2, Vector3):
            raise ValueError("vect_1 must be a Vector3!")
        
        if vect_1.is_multiple(vect_2):
            raise ValueError("vect_1 and vect_2 cannot be scalar multiples of each other!")
        
        if not isinstance(point, Vector3):
            raise ValueError("point must be a Vector3!")
        
        self.v1 = vect_1
        self.v2 = vect_2
        self.normal = Vector3.cross(vect_1,vect_2)
        self.point = point

    def in_plane(self, point):
        if not isinstance(point, Vector3):
            raise ValueError("point must be a Vector3!")
        
        point_vect = point - self.point

        if abs(Vector3.dot(point_vect, self.normal)) < EPS:
            return True
        
        return False