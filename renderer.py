import open3d as o3d
import numpy as np

def main():
    N = 5
    vertices = o3d.utility.Vector3dVector(
        np.array([[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1], [0.5, 0.5, 0.5]]))
    triangles = o3d.utility.Vector3iVector(
        np.array([[0, 1, 2], [0, 2, 3], [0, 4, 1], [1, 4, 2], [2, 4, 3],
                  [3, 4, 0]]))
    mesh_np = o3d.geometry.TriangleMesh(vertices, triangles)
    mesh_np.vertex_colors = o3d.utility.Vector3dVector(
        np.random.uniform(0, 1, size=(N, 3)))
    mesh_np.compute_vertex_normals()
    print(np.asarray(mesh_np.triangle_normals))
    print("Displaying mesh made using numpy ...")
    o3d.visualization.draw_geometries([mesh_np])

if __name__ == "__main__":
    main()