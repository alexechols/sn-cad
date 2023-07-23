from vector import *
import copy

class Polygon:
    def __init__(self, points):
        if not isinstance(points, (list, tuple)):
            raise ValueError(f"Unsupported point list type {type(points)}")
        
        if len(points) <= 2:
            raise ValueError(f"Polygon may not be constructed from fewer than 3 points, {len(points)} given")
        
        self.points = []
        self.sides = []
        self.ccw = True
        self.convex = True
        self.centroid = Vector2(0, 0)

        prev_cross_mag = 0
        delta_ang = 0

        for point in points:
            if not isinstance(point, (Vector2, list, tuple)):
                raise ValueError(f"Unsupported point type {type(point)}")
            
            if isinstance(point, Vector2):
                self.points.append(point)

            else:
                if len(point) != 2:
                    raise ValueError(f"Received point of size {len(point)}. Expected size 2")
                
                self.points.append(Vector2(*point))
            
            self.centroid += self.points[-1]

            if len(self.points) > 1:
                self.sides.append(self.points[-1] - self.points[-2])

            if len(self.sides) > 1:
                if abs(Vector2.angle_between(self.sides[-1], self.sides[-2])) < EPS:
                    self.points.pop(-2)
                    self.sides.pop(-1)
                    self.sides.pop(-1)
                    self.sides.append(self.points[-1] - self.points[-2])

                else:
                    cross = Vector2.signed_cross_mag(self.sides[-2], self.sides[-1])
                    if abs(cross) >= EPS:
                        cross_mag = cross/abs(cross)
                        delta_ang += Vector2.angle_between(self.sides[-2],self.sides[-1]) * cross_mag

                        if (cross_mag > 0 and prev_cross_mag < 0) or (cross_mag < 0 and prev_cross_mag > 0):
                            self.convex = False

                        prev_cross_mag = cross_mag
                    else:
                        raise ValueError("Polygon is not valid, vertex cannot form an angle of zero degrees")

        self.sides.append(self.points[0] - self.points[-1])

        self.centroid = self.centroid/len(self.points)

        cross = Vector2.signed_cross_mag(self.sides[-2], self.sides[-1])
        cross_mag = cross/abs(cross)
        delta_ang += Vector2.angle_between(self.sides[-2],self.sides[-1]) * cross_mag

        if (cross_mag > 0 and prev_cross_mag < 0) or (cross_mag < 0 and prev_cross_mag > 0):
            self.convex = False

        if delta_ang > 0:
            self.ccw = True
        
        elif delta_ang < 0:
            self.ccw = False

        else:
            raise ValueError("Given polygon has an overall delta angle of zero")
        
    def __repr__(self):
        out = "{"
        for point in self.points:
            out = out + str(point) + ", "
        out = out[:-2] + "}"

        return out
    
    def is_inside(self, point):
        if not isinstance(point, (Vector2, tuple, list)):
            raise ValueError(f"Point should be of type Vector2, tuple, or list not of type {type(point)}")
        
        if isinstance(point, (list, tuple)):
            if len(point) != 2:
                raise ValueError(f"Point should be of length 2, not {len(point)}")
            
            if not isinstance(point[0], (int,float)) or not isinstance(point[1], (int, float)):
                raise ValueError(f"Point must contain only ints or floats, not objects of type(s) {type(point[0])} and {type(point[1])}")
            
            point = Vector2(*point)

        cross_counter = 0
        for i in range(len(self.points)):
            start = self.points[i-1]
            end = self.points[i] 

            if point.x < start.x and point.x < end.x:
                if point.y < start.y and point.y > end.y or point.y > start.y and point.y < end.y:
                    cross_counter += 1
            
            elif (point.x < start.x and point.x > end.x) or (point.x > start.x and point.x < end.x):

                t = Vector2.rev_lerp(start.x, end.x, point.x)
                close_point = Vector2.lerp(start, end, t)

                if start.x < point.x and ((point.y > end.y and point.y < close_point.y) or (point.y < end.y and point.y > close_point.y)):
                    cross_counter += 1
                    
                elif start.x > point.x and ((point.y > start.y and point.y < close_point.y) or (point.y < start.y and point.y > close_point.y)):
                    cross_counter += 1

        return bool(cross_counter % 2)
    
    def split_between(self, ind_1, ind_2):
        if not isinstance(ind_1, int) or not isinstance(ind_2, int):
            raise ValueError("Vertex indices must be integers!")
        
        if ind_1 >= len(self.points):
            raise IndexError("Index 1 out of range!")
        
        if ind_2 >= len(self.points):
            raise IndexError("Index 2 out of range!")
        
        if ind_1 == ind_2:
            raise ValueError("Indices must not be equal!")
        
        if ind_1 < ind_2:
            poly_1 = Polygon(self.points[ : ind_1 + 1] + self.points[ind_2 : ])
            poly_2 = Polygon(self.points[ind_1 : ind_2+1])
        else:
            poly_1 = Polygon(self.points[ : ind_2 + 1] + self.points[ind_1 : ])
            poly_2 = Polygon(self.points[ind_2 : ind_1+1])

        return (poly_1, poly_2)
    
    @staticmethod
    def reverse(poly):
        if not isinstance(poly, Polygon):
            raise ValueError(f"reverse can only be applied to objects of type Polygon, not {type(poly)}")
        
        return Polygon(poly.points[:1] + poly.points[:0:-1])
    
    def convex_hull(self):
        if self.ccw:
            return Polygon.reverse(self).convex_hull()
        
        remaining_inds = set(range(len(self.points)))
        hull_inds = []
        hull_points = []

        min_ind = 0

        for ind in remaining_inds:
            if self.points[ind].x < self.points[min_ind].x:
                min_ind = ind

            elif (self.points[ind].x == self.points[min_ind].x) and (self.points[ind].y < self.points[min_ind].y):
                min_ind = ind

        hull_inds.append(min_ind)
        hull_points.append(self.points[min_ind])

        for i in range(len(self.points)):
            if i == 0:
                major_pointer = Vector2(-1,0)
            
            min_ang = 2*math.pi
            min_ind = hull_inds[i]

            for j in remaining_inds:
                if j == hull_inds[i]:
                    continue 

                minor_pointer = self.points[j] - self.points[hull_inds[i]]

                ang = Vector2.ccw_angle_between(minor_pointer, major_pointer, Vector3(0, 0, 1))

                if ang < min_ang:
                    min_ang = ang
                    min_ind = j

            hull_inds.append(min_ind)
            hull_points.append(self.points[min_ind])
            remaining_inds.remove(min_ind)

            if hull_inds[-1] == hull_inds[0]:
                break
        
        return Polygon(hull_points[:-1])
    
    def othogonality(self):
        ortho_count = 0

        for i in range(len(self.sides)):
            ang = Vector2.angle_between(self.sides[i-1],self.sides[i])
            if abs(ang % math.pi/2) < EPS:
                ortho_count += 1

        return ortho_count/len(self.sides)
    
    def project(self, to_plane, from_plane):
        if not isinstance(to_plane, Plane):
            raise ValueError("to_plane must be a Plane!")
        
        if not isinstance(from_plane, Plane):
            raise ValueError("from_plane must be a Plane!")
        
        from_proj_points = self._project_into(from_plane)
        to_proj_points = []

        for point in from_proj_points:
            t_intersect = Vector3.dot(to_plane.point - point, to_plane.normal)/Vector3.dot(to_plane.normal, to_plane.normal)

            proj_point = point + to_plane.normal * t_intersect

            to_proj_points.append(proj_point)

        return Polygon._project_out_of(to_proj_points, to_plane)
        
    def _project_into(self, plane):
        if not isinstance(plane, Plane):
            raise ValueError("plane must be a Plane!")
        
        proj_points = []

        for point in self.points:
            proj_point = Vector3(point.x * plane.v1.x + point.y * plane.v2.x, 
                                 point.x * plane.v1.y + point.y * plane.v2.y, 
                                 point.x * plane.v1.z + point.y * plane.v2.z)
            
            proj_points.append(proj_point + plane.point)

    @staticmethod
    def _project_out_of(proj_points, plane):
        if not isinstance(plane, Plane):
            raise ValueError("plane must be a Plane!")
        
        if not isinstance(proj_points, list[Vector3]):
            raise ValueError("proj_points must be a list of Vector3s")
        
        det = Vector3.dot(plane.normal, plane.normal)

        v1_cross = Vector3.cross(plane.v1, plane.normal)
        v2_cross = Vector3.cross(plane.v2, plane.normal)

        new_points = []

        for proj_point in proj_points:
            point = proj_point - plane.point

            new_point = Vector2(
                plane.normal.z * point.x - v1_cross.z * point.y + v2_cross.z * point.z,
                plane.normal.y * point.x - v1_cross.y * point.y + v2_cross.y * point.z
            )/det

            new_points.append(new_point)

        return Polygon(new_points)
        

