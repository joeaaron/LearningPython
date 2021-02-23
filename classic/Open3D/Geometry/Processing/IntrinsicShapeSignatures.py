import open3d_tutorial as o3dtut
import open3d as o3d
import time

# Compute ISS Keypoints on Armadillo
mesh = o3dtut.get_armadillo_mesh()
pcd = o3d.geometry.PointCloud()
pcd.points = mesh.vertices

tic = time.time()
keypoints = o3d.geometry.keypoint.compute_iss_keypoints(pcd)
toc = 1000 * (time.time() - tic)
print("ISS Computation took {:.0f} [ms]".format(toc))

mesh.compute_vertex_normals()
mesh.paint_uniform_color([0.5, 0.5, 0.5])
keypoints.paint_uniform_color([1.0, 0.75, 0.0])
o3d.visualization.draw_geometries([keypoints, mesh], front=[0, 0, -1.0])
