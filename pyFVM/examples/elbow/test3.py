from src.readData import read_poly_mesh

if __name__ == "__main__":
    mm = read_poly_mesh()
    mm()
    print(mm.the_number_of_boundaryElements)