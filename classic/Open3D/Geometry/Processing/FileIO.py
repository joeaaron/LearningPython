import open3d as o3d

# Point Cloud
print("Testing IO for point cloud ...")
pcd = o3d.io.read_point_cloud("../../test_data/fragment.pcd")
print(pcd)
o3d.io.write_point_cloud("copy_of_fragment.pcd", pcd)

# Mesh
print("Testing IO for meshes ...")
mesh = o3d.io.read_triangle_mesh("../../test_data/knot.ply")
print(mesh)
o3d.io.write_triangle_mesh("copy_of_knot.ply", mesh)

# Image
print("Testing IO for images ...")
img = o3d.io.read_image("../../test_data/lena_color.jpg")
print(img)
o3d.io.write_image("copy_of_lena_color.jpg", img)