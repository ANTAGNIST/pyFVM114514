class ElementsGrad:
    def __init__(self, mesh, facesPhi):
        self.the_number_of_internalFaces = mesh.the_number_of_internalFaces
        self.the_number_of_faces = mesh.the_number_of_faces
        self.the_number_of_elements = mesh.the_number_of_elements
        self.facesSf = mesh.facesSf
        self.facesID2ownerElementsID = mesh.facesID2ownerElementsID
        self.facesID2neighbourElementsID = mesh.facesID2neighbourElementsID
        self.elementsVolume = mesh.elementsVolume
        self.facesPhi = facesPhi

    def calculate(self):
        self.elementsGrad = [[0] for _ in range(self.the_number_of_elements)]
        # 对内部面循环
        for facesID in range(self.the_number_of_internalFaces):
            face_flux = self.facesPhi[facesID] * self.facesSf[facesID]#####
            elementsID1 = self.facesID2ownerElementsID[facesID][0]
            elementsID2 = self.facesID2neighbourElementsID[facesID][0]
            if elementsID1 < elementsID2:
                self.elementsGrad[elementsID1] -= face_flux
                self.elementsGrad[elementsID2] += face_flux
            elif elementsID1 > elementsID2:
                self.elementsGrad[elementsID1] += face_flux
                self.elementsGrad[elementsID2] -= face_flux
            else:
                print("Error: elementsID1==elementsID2, please check out self.facesID2ownerElementsID and self.facesID2neighbourElementsID or their resource file onwer and neighbour")
                break
        # 对边界面循环
        for facesID in range(self.the_number_of_internalFaces, self.the_number_of_faces):
            face_flux = self.facesPhi[facesID] * self.facesSf[facesID]#####
            elementsID1 = self.facesID2ownerElementsID[facesID][0]
            self.elementsGrad[elementsID1] += face_flux
        # 对单元做循环
        for elementsID in range(self.the_number_of_elements):
            self.elementsGrad[elementsID][0] /= self.elementsVolume[elementsID][0]

        return self.elementsGrad


