import open3d as o3d

print("Load a pcd point cloud, print it, and render it")
pcd = o3d.io.read_point_cloud("calibrated_pointcloud_13_49_07.pcd")
print(pcd)
o3d.visualization.draw_geometries([pcd])