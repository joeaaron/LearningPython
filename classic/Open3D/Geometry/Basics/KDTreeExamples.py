import open3d as o3d
import numpy as np

print("Testing kdtree in Open3D...")
print("Load a point cloud and paint it gray.")
pcd = o3d.io.read_point_cloud("./test_data/Feature/cloud_bin_0.pcd")
pcd.paint_uniform_color([0.5,0.5,0.5])
pcd_tree = o3d.geometry.KDTreeFlann(pcd)

print("Paint the 1500th point red.")
pcd.colors[1500] = [1, 0, 0]

# Using search_knn_vector_3d
print("Find its 200 nearest neighbors, and paint them blue.")
[k, idx, _] = pcd_tree.search_knn_vector_3d(pcd.points[1500], 200)
np.asarray(pcd.colors)[idx[1:], :] = [0, 0, 1]

# Using search_radius_vector_3d
print("Find its neighbors with distance less than 0.2, and paint them green.")
[k, idx, _] = pcd_tree.search_radius_vector_3d(pcd.points[1500], 0.2)
np.asarray(pcd.colors)[idx[1:], :] = [0, 1, 0]

print("Visualize the point cloud.")
o3d.visualization.draw_geometries([pcd])