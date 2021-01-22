import open3d as o3d
import open3d_tutorial as o3dtut
import numpy as np
import matplotlib.pyplot as plt

# 1.Visualize point cloud
#pcd = o3d.io.read_point_cloud("./test_data/ICP/cloud_bin_0.pcd")
print("Load a ply point cloud, print it, and render it")
pcd = o3d.io.read_point_cloud("../../test_data/fragment.ply")
print(pcd)
print(np.asarray(pcd.points))
#o3d.visualization.draw_geometries([pcd])

# 2.Voxel downsampling
print("Downsample the point cloud with a voxel of 0.05")
downpcd = pcd.voxel_down_sample(voxel_size=0.05)
#o3d.visualization.draw_geometries([downpcd])

# 3.Vertex normal estimation
print("Recompute the normal of the downsampled point cloud")
downpcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
#o3d.visualization.draw_geometries([downpcd])

# 4.Crop point cloud
print("Load a polygon volume and use it to crop the original point cloud")
vol = o3d.visualization.read_selection_polygon_volume("../../test_data/Crop/cropped.json")
chair = vol.crop_point_cloud(pcd)
#o3d.visualization.draw_geometries([chair])
dists = pcd.compute_point_cloud_distance(chair)
dists = np.asarray(dists)
ind = np.where(dists > 0.01)[0]
pcd_without_chair = pcd.select_by_index(ind)
#o3d.visualization.draw_geometries([pcd_without_chair])

# 5.Paint point cloud
print("Paint chair")
chair.paint_uniform_color([1, 0.706, 0])         # paints all the points to a uniform color. The color is in RGB space, [0, 1] range.
#o3d.visualization.draw_geometries([chair])

# 6.Bounding volumes
aabb = chair.get_axis_aligned_bounding_box()
aabb.color = (1,0,0)
obb = chair.get_oriented_bounding_box()
obb.color = (0,1,0)
#o3d.visualization.draw_geometries([chair, aabb, obb])

# 7.Convex hull
pcl = o3dtut.get_bunny_mesh().sample_points_poisson_disk(number_of_points=2000)
hull, _ = pcl.compute_convex_hull()
hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
hull_ls.paint_uniform_color((1, 0, 0))
#o3d.visualization.draw_geometries([pcl, hull_ls])

# 8.DBSCAN clustering
with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    labels = np.array(pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))
max_label = labels.max()
print(f"point cloud has {max_label + 1} clusters")
colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
colors[labels < 0] = 0
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
#o3d.visualization.draw_geometries([pcd])

# 9.Plane segmentation
pcd = o3d.io.read_point_cloud("../../test_data//fragment.pcd")
plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,
                                         ransac_n=3,
                                         num_iterations=1000)
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

inlier_cloud = pcd.select_by_index(inliers)
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud = pcd.select_by_index(inliers, invert=True)
o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])