from polygon import *
import matplotlib.pyplot as plt

def main():
    #test_poly = Polygon(([0,0],[0,1],[0.5,0.5],[1,1],[1.25,0.5],[1.75,1.75],[2,-1],[1,0],[0,-1]))
    #test_poly = Polygon(([0,0],[0,1],[1,1],[2,-1],[1,0],[0,-1]))
    #test_poly = Polygon.reverse(test_poly)
    test_poly = Polygon(([0,0], [0,10], [21, 10], [21, 0], [16, 0], [16,3], [5,3]))
    for i, point in enumerate(test_poly.points):
        plt.scatter([point.x],[point.y],color="black")
        plt.arrow(point.x, point.y, test_poly.sides[i].x, test_poly.sides[i].y, color="black",length_includes_head=True, width=0.007)

    hull = test_poly.convex_hull()
    for i, point in enumerate(hull.points):
        plt.scatter([point.x],[point.y],color="red")
        plt.arrow(point.x, point.y, hull.sides[i].x, hull.sides[i].y, color="red",length_includes_head=True, width=0.007)

    # inside = test_inside(test_poly, [[-2,3],[-2,3]],17)
    # in_x = []
    # in_y = []
    # out_x = []
    # out_y = []

    # for key in inside.keys():
    #     if inside[key] == True:
    #         in_x.append(key[0])
    #         in_y.append(key[1])
    #     else:
    #         out_x.append(key[0])
    #         out_y.append(key[1])

    # plt.scatter(in_x,in_y,color="green")
    # plt.scatter(out_x, out_y, color="red")
    
    plt.show()

def test_inside(poly, bounds, num_points):
    x_w = (bounds[0][1] - bounds[0][0])/num_points
    y_w = (bounds[1][1] - bounds[1][0])/num_points

    inside_dict = {}

    for x in range(num_points + 1):
        for y in range(num_points + 1):
            inside_dict[(bounds[0][0] + x*x_w, bounds[1][0] + y*y_w)] = poly.is_inside((bounds[0][0] + x*x_w, bounds[1][0] + y*y_w))

    return inside_dict

if __name__ == "__main__":
    main()