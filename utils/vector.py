import math
import sys

EPS = 2*sys.float_info.epsilon

class Vector3:
    def __init__(self, x, y, z):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or not isinstance(z, (int, float)):
            raise ValueError(f"Cannot define {type(self)} with elements of type(s) {type(x)}, {type(y)}, and {type(z)}")
        
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if not isinstance(other, Vector3):
            return False
        
        return (abs(self.x - other.x) < EPS and abs(self.y - other.y) < EPS) and abs(self.z - other.z) < EPS
    
    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError(f"Multiplication is not defined for {type(self)} and object of type {type(other)}")
        
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError(f"Multiplication is not defined for {type(self)} and object of type {type(other)}")
        
        if abs(other) < EPS:
            raise ZeroDivisionError()
    
        return Vector3(self.x/other, self.y/other, self.z/other)
    
    def __add__(self, other):
        if not isinstance(other, (Vector3, int, float)):
            raise ValueError(f"Addition is not defined for {type(self)} and object of type {type(other)}")
        
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        
        return Vector2(self.x + other, self.y + other, self.z + other.z)
    
    def __sub__(self, other):
        if not isinstance(other, (Vector3, int, float)):
            raise ValueError(f"Subtraction is not defined for {type(self)} and object of type {type(other)}")
        
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        
        return Vector2(self.x - other, self.y - other)
    
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    
    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2) 
    
    def __str__(self):
        return f"<{self.x}, {self.y}, {self.z}>"
    
    def __repr__(self):
        return f"<{self.x}, {self.y}, {self.z}>"
    
    def is_multiple(self, other):
        if not isinstance(other, Vector3):
            raise ValueError(f"Vector3 cannot be a multiple of {type(other)}")
        
        if abs(self.x) < EPS and abs(self.y) < EPS and abs(self.z) < EPS:
            return True
        
        if abs(self.x) > EPS:
            ratio = other.x/self.x
        elif abs(self.y) > EPS:
            ratio = other.y/self.y
        else:
            ratio = other.z/self.z

        if abs(abs(self.x * ratio) - abs(other.x)) < EPS and abs(abs(self.y * ratio) - abs(other.y)) < EPS and abs(abs(self.z * ratio) - abs(other.z)) < EPS:
            return True
        
        return False

    def decompose(self):
        #returns the series of euler angles and a scale factor which yield the given vector when applied to Vector3(1, 0, 0)
        xy_proj = Vector3(self.x, self.y, 0)

        try:
            theta = Vector3.ccw_angle_between(Vector3(1,0,0), xy_proj, Vector3(0,0,1))
        
        except:
            theta = 0

        rot_vect = Vector3(1,0,0).rot_about_z(theta)

        try:
            phi = Vector3.ccw_angle_between(rot_vect, self, Vector3(0,0,1))
        
        except:
            phi = 0

    def rot_about_x(self, theta):
        return Vector3(
            self.x,
            self.y * math.cos(theta) - self.z * math.sin(theta),
            self.y * math.sin(theta) + self.z * math.cos(theta)
        )
    
    def rot_about_y(self, theta):
        return Vector3(
            self.x * math.cos(theta) + self.z * math.sin(theta),
            self.y,
            -self.x * math.sin(theta) + self.z * math.cos(theta)
        )
    
    def rot_about_z(self, theta):
        return Vector3(
            self.x * math.cos(theta) - self.y * math.sin(theta),
            self.x * math.sin(theta) + self.x * math.cos(theta),
            self.z
        )

    @staticmethod
    def dot(vect_1, vect_2):
        if not isinstance(vect_1, Vector3) or not isinstance(vect_2, Vector3):
            raise ValueError(f"Dot product is not defined for {type(vect_1)} and {type(vect_2)}")
        
        return vect_1.x * vect_2.x + vect_1.y * vect_2.y + vect_1.z * vect_2.z
    
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
    def cross(vect_1, vect_2):
        if not isinstance(vect_1, Vector3) or not isinstance(vect_2, Vector3):
            raise ValueError(f"Cross product is not defined for objects of type {type(vect_1)} and {type(vect_2)}")
        
        return Vector3(vect_1.y * vect_2.z - vect_1.z * vect_2.y, vect_1.z * vect_2.x - vect_1.z * vect_2.z, vect_1.x * vect_2.y - vect_1.y * vect_2.x)
    
    @staticmethod
    def ccw_angle_between(vect_1, vect_2, plane_normal):
        if not isinstance(vect_1, Vector3) or not isinstance(vect_2, Vector3) or not isinstance(plane_normal, Vector3):
            raise ValueError(f"Angle between is not defined for vectors of type(s) {type(vect_1)} and {type(vect_2)}, and plane normal of type {type(plane_normal)}")
        
        cross = Vector3.cross(vect_1, vect_2)
        if not plane_normal.is_multiple(cross):
            raise ValueError(f"Plane Normal must be a real multiple of the cross product of vect_1 and vect_2")
        
        if plane_normal.norm() < EPS:
            raise ValueError("Normal vector cannot have 0 magnitude!")
        unit_normal = plane_normal/plane_normal.norm()

        signed_ang = math.atan2(Vector3.dot(cross, unit_normal), Vector3.dot(vect_1, vect_2))

        if signed_ang >= 0:
            return signed_ang
        else:
            return 2*math.pi + signed_ang

    
class Vector2(Vector3):
    def __init__(self, x, y):
        super().__init__(x, y, 0)

    @staticmethod
    def signed_cross_mag(vect_1, vect_2):
        if not isinstance(vect_1, Vector3) or not isinstance(vect_2, Vector3):
            raise ValueError(f"Cross product is not defined for objects of type(s) {type(vect_1)} and {type(vect_2)}")

        return Vector3.cross(vect_1, vect_2).z

    