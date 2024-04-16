from .readConstantFile import read_faces_file, read_boundary_file, read_neighbour_file, read_owner_file, read_points_file
from src.calculate import CalculateTopology

def read_poly_mesh(
        neighbour_path:str="./neighbour",
        owner_path:str="./owner",
        faces_path:str="./faces",
        points_path:str="./points",
        boundary_path:str="./boundary",
) -> object:
    facesID2neighbourElementsID, the_number_of_internalFaces, the_number_of_elements = read_neighbour_file(neighbour_path)
    facesID2ownerElementsID, the_number_of_faces = read_owner_file(owner_path)
    facesID2pointsID, _ = read_faces_file(faces_path)  # _ == the_number_of_faces
    pointsCoordinate, the_number_of_points = read_points_file(points_path)
    boundary_dict, the_number_of_boundaries = read_boundary_file(boundary_path)

    mesh = CalculateTopology()
    mesh.facesID2neighbourElementsID = facesID2neighbourElementsID
    mesh.facesID2ownerElementsID = facesID2ownerElementsID
    mesh.facesID2pointsID = facesID2pointsID
    mesh.pointsCoordinate = pointsCoordinate
    mesh.boundary_dict = boundary_dict

    mesh.the_number_of_internalFaces = the_number_of_internalFaces
    mesh.the_number_of_elements = the_number_of_elements
    mesh.the_number_of_faces = the_number_of_faces
    mesh.the_number_of_points = the_number_of_points
    mesh.the_number_of_boundaries = the_number_of_boundaries
    return mesh
