import open3d_tutorial as o3dtut
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

# Alpha shapes
mesh = o3dtut.get_bunny_mesh()
pcd = mesh.sample_points_poisson_disk(750)
#o3d.visualization.draw_geometries([pcd])
alpha = 0.03
print(f"alpha={alpha:.3f}")
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
mesh.compute_vertex_normals()
#o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
for alpha in np.logspace(np.log10(0.5), np.log10(0.01), num=4):
    print(f"alpha={alpha:.3f}")
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
        pcd, alpha, tetra_mesh, pt_map)
    mesh.compute_vertex_normals()
    #o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

# Ball pivoting
gt_mesh = o3dtut.get_bunny_mesh()
gt_mesh.compute_vertex_normals()
pcd = gt_mesh.sample_points_poisson_disk(3000)
#o3d.visualization.draw_geometries([pcd])

radii = [0.005, 0.01, 0.02, 0.04]
rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector(radii))
#o3d.visualization.draw_geometries([pcd, rec_mesh])

# Poisson surface reconstruction
pcd = o3dtut.get_eagle_pcd()
print(pcd)
#o3d.visualization.draw_geometries([pcd])

print('run Poisson surface reconstruction')
with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=9)
print(mesh)
#o3d.visualization.draw_geometries([mesh])

print('visualize densities')
densities = np.asarray(densities)
density_colors = plt.get_cmap('plasma')(
    (densities - densities.min()) / (densities.max() - densities.min()))
density_colors = density_colors[:, :3]
density_mesh = o3d.geometry.TriangleMesh()
density_mesh.vertices = mesh.vertices
density_mesh.triangles = mesh.triangles
density_mesh.triangle_normals = mesh.triangle_normals
density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
#o3d.visualization.draw_geometries([density_mesh])

print('remove low density vertices')
vertices_to_remove = densities < np.quantile(densities, 0.01)
mesh.remove_vertices_by_mask(vertices_to_remove)
print(mesh)
#o3d.visualization.draw_geometries([mesh])

# Normal estimation
gt_mesh = o3dtut.get_bunny_mesh()
pcd = gt_mesh.sample_points_poisson_disk(5000)
pcd.normals = o3d.utility.Vector3dVector(np.zeros(
    (1, 3)))  # invalidate existing normals

pcd.estimate_normals()
o3d.visualization.draw_geometries([pcd], point_show_normal=True)

pcd.orient_normals_consistent_tangent_plane(100)
o3d.visualization.draw_geometries([pcd], point_show_normal=True)