import numpy as np
from typing import List

from src.readData.utils import unique

class CalculateTopology:
    def __init__(self):
        self.facesID2neighbourElementsID = None  # neighbour
        self.facesID2ownerElementsID = None  # owner
        self.facesID2pointsID = None  # faces
        self.pointsCoordinate = None  # points
        self.boundary_dict = None  # boundary

        self.the_number_of_internalFaces = None  # neighbour
        self.the_number_of_elements = None  # owner
        self.the_number_of_faces = None  # faces
        self.the_number_of_points = None  # points
        self.the_number_of_boundaries = None  # boundary

        self.the_number_of_boundaryElements = None
        self.elementID2neighboursElementID = None
        self.elementID2facesID = None
        self.elementsID2pointsID = None
        self.upperAnbCoeffID = None
        self.lowerAnbCoeffID = None
        self.pointsID2elementsID = None
        self.pointsID2facesID = None
        self.elementsCentroCoordinate = None
        self.elementsVolume = None
        self.facesCentroCoordinate = None
        self.facesSf = None
        self.facesArea = None
        self.facesWeights = None
        self.facesCf = None
        self.facesFf = None
        self.facesCF = None
        self.facesWallDist = None
        self.facesWallDistLimited = None

        # ProcessElementTopology

    def calculate_the_number_of_boundaryElements(self):
        # the_number_of_boundaryElements == the_number_of_boundaryFaces
        self.the_number_of_boundaryElements = self.the_number_of_faces - self.the_number_of_internalFaces

    def calculate_elementsID2neighbourElementsID(self):
        self.elementID2neighboursElementID = [[] for _ in range(self.the_number_of_elements)]
        for faceID in range(self.the_number_of_internalFaces):
            ownElementID = self.facesID2ownerElementsID[faceID][0]
            neiElementID = self.facesID2neighbourElementsID[faceID][0]
            self.elementID2neighboursElementID[ownElementID].append(neiElementID)
            self.elementID2neighboursElementID[neiElementID].append(ownElementID)

    def calculate_elementsID2facesID(self):
        self.elementID2facesID = [[] for _ in range(self.the_number_of_elements)]
        for faceID in range(self.the_number_of_internalFaces):
            ownElementID = self.facesID2ownerElementsID[faceID][0]
            neiElementID = self.facesID2neighbourElementsID[faceID][0]
            self.elementID2facesID[ownElementID].append(faceID)
            self.elementID2facesID[neiElementID].append(faceID)
        for faceID in range(self.the_number_of_internalFaces, self.the_number_of_faces):
            ownElementID = self.facesID2ownerElementsID[faceID][0]
            self.elementID2facesID[ownElementID].append(faceID)

    def calculate_elementsID2pointsID(self):
        self.elementsID2pointsID = [[] for _ in range(self.the_number_of_elements)]
        for elementID in range(self.the_number_of_elements):
            faceIDs = self.elementID2facesID[elementID]
            for faceID in faceIDs:
                pointsIDs = self.facesID2pointsID[faceID]
                self.elementsID2pointsID[elementID].extend(pointsIDs)
            self.elementsID2pointsID[elementID] = unique(self.elementsID2pointsID[elementID])

    def calculate_upperAnbCoeffID_and_lowerAnbCoeffID(self):
        self.upperAnbCoeffID = [[] for _ in range(self.the_number_of_internalFaces)]
        self.lowerAnbCoeffID = [[] for _ in range(self.the_number_of_internalFaces)]
        for elementID in range(self.the_number_of_elements):
            NbID = 1
            for faceID in self.elementID2facesID[elementID]:
                # 跳过边界面
                if faceID > self.the_number_of_internalFaces - 1:
                    continue
                ownElementID = self.facesID2ownerElementsID[faceID][0]
                neiElementID = self.facesID2neighbourElementsID[faceID][0]
                if elementID == ownElementID:
                    self.upperAnbCoeffID[faceID].append(NbID)
                elif elementID == neiElementID:
                    self.lowerAnbCoeffID[faceID].append(NbID)
                NbID += 1
        # ProcessNodeTopology

    def calculate_pointsID2elementsID(self):
        self.pointsID2elementsID = [[] for _ in range(self.the_number_of_points)]
        for elementsID in range(self.the_number_of_elements):
            pointsIDs = self.elementsID2pointsID[elementsID]
            for pointsID in pointsIDs:
                self.pointsID2elementsID[pointsID].append(elementsID)

    def calculate_pointsID2facesID(self):
        self.pointsID2facesID = [[] for _ in range(self.the_number_of_points)]
        for facesID in range(self.the_number_of_faces):
            pointsIDs = self.facesID2pointsID[facesID]
            for pointID in pointsIDs:
                self.pointsID2facesID[pointID].append(facesID)
        # ProcessGeometry

    def calculate_elementsCentroCoordinate_and_elementsVolume(self):
        self.elementsCentroCoordinate: list = [[] for _ in range(self.the_number_of_elements)]
        self.elementsVolume: list = [[] for _ in range(self.the_number_of_elements)]
        for elementsID in range(self.the_number_of_elements):
            facesIDs = self.elementID2facesID[elementsID]
            polyheronElementRoughCentroCoord: np.ndarray = np.array([0, 0, 0])

            for facesID in facesIDs:
                polyheronElementRoughCentroCoord = polyheronElementRoughCentroCoord + np.array(
                    self.facesCentroCoordinate[facesID])
            polyheronElementRoughCentroCoord = polyheronElementRoughCentroCoord / len(facesIDs)

            pyramidCentroCoord: np.ndarray = np.array([0, 0, 0])
            pyramidVolume: float = 0
            sum_pyramidCentroCoord_dot_pyramidVolume = np.array([0, 0, 0])
            sum_pyramidVolume: float = 0
            for facesID in facesIDs:
                # owner代表起点，neighbour代表终点，facesSf的ID对应facesIDelemnetsID
                faceSign = 1
                if self.facesID2ownerElementsID[facesID][0] != elementsID:
                    faceSign = -1
                pyramidCentroCoord: np.ndarray = (3 / 4) * np.array(self.facesCentroCoordinate[facesID]) + (
                            1 / 4) * polyheronElementRoughCentroCoord
                pyramidVolume: float = (1 / 3) * np.dot(
                    (np.array(self.facesCentroCoordinate[facesID]) - polyheronElementRoughCentroCoord),
                    np.array(self.facesSf[facesID]) * faceSign
                )
                sum_pyramidCentroCoord_dot_pyramidVolume = sum_pyramidCentroCoord_dot_pyramidVolume + np.dot(
                    pyramidCentroCoord, pyramidVolume)
                sum_pyramidVolume = sum_pyramidVolume + pyramidVolume
            polyheronElemnetCentroCoord = sum_pyramidCentroCoord_dot_pyramidVolume / sum_pyramidVolume

            self.elementsCentroCoordinate[elementsID].extend(list(polyheronElemnetCentroCoord))
            self.elementsVolume[elementsID].append(float(sum_pyramidVolume))

    def calculate_facesCentroCoordinate_and_facesSf_and_facesArea(self):
        self.facesCentroCoordinate = [[] for _ in range(self.the_number_of_faces)]
        self.facesSf = [[] for _ in range(self.the_number_of_faces)]
        self.facesArea = [[] for _ in range(self.the_number_of_faces)]
        for facesID in range(self.the_number_of_faces):
            pointsIDs = self.facesID2pointsID[facesID]
            polygonFacesRoughCentroCoord: np.ndarray = np.array([0, 0, 0])
            subTriangleFacesSf: np.ndarray = np.array([0, 0, 0])
            subTriangleFacesArea: float = 0

            sum_Sf: np.ndarray = np.array([0, 0, 0])
            sum_Area: float = 0
            sum_xDotArea: np.ndarray = np.array([0, 0, 0])

            for pointsID in pointsIDs:
                polygonFacesRoughCentroCoord = polygonFacesRoughCentroCoord + np.array(self.pointsCoordinate[pointsID])
            polygonFacesRoughCentroCoord = polygonFacesRoughCentroCoord / len(pointsIDs)
            for subTriangleID in range(len(pointsIDs)):
                x0: np.ndarray = polygonFacesRoughCentroCoord
                if subTriangleID == len(pointsIDs) - 1:
                    x1: np.ndarray = np.array(self.pointsCoordinate[pointsIDs[subTriangleID]])
                    x2: np.ndarray = np.array(self.pointsCoordinate[pointsIDs[0]])
                else:
                    x1: np.ndarray = np.array(self.pointsCoordinate[pointsIDs[subTriangleID]])
                    x2: np.ndarray = np.array(self.pointsCoordinate[pointsIDs[subTriangleID + 1]])
                subTriangleFacesSf = (1 / 2) * np.cross(x1 - x0, x2 - x0)
                subTriangleFacesArea = np.linalg.norm(subTriangleFacesSf)

                sum_Sf = sum_Sf + subTriangleFacesSf
                sum_Area = sum_Area + subTriangleFacesArea
                sum_xDotArea = sum_xDotArea + np.dot((1 / 3) * (x0 + x1 + x2), subTriangleFacesArea)

            self.facesSf[facesID].extend(list(sum_Sf))
            self.facesArea[facesID].append(float(sum_Area))

            facesCentroCoordinate = sum_xDotArea / sum_Area
            self.facesCentroCoordinate[facesID].extend(list(facesCentroCoordinate))

    def calculate_facesWeights_and_facesWallDist_and_facesWallDistLimited(self):
        self.facesWeights = [[] for _ in range(self.the_number_of_faces)]
        self.facesCf = [[] for _ in range(self.the_number_of_faces)]
        self.facesFf = [[] for _ in range(self.the_number_of_faces)]
        self.facesCF = [[] for _ in range(self.the_number_of_faces)]

        for facesID in range(self.the_number_of_internalFaces):
            facesUnitVector = np.array(self.facesSf[facesID]) / np.array(self.facesArea[facesID])
            # 提取facesID旁边的两个elementID
            ownElementID = self.facesID2ownerElementsID[facesID][0]
            neiElemnetID = self.facesID2neighbourElementsID[facesID][0]
            facesCf = np.array(self.facesCentroCoordinate[facesID]) - np.array(
                self.elementsCentroCoordinate[ownElementID])
            facesFf = np.array(self.facesCentroCoordinate[facesID]) - np.array(
                self.elementsCentroCoordinate[neiElemnetID])
            facesCF = np.array(self.elementsCentroCoordinate[neiElemnetID]) - np.array(
                self.elementsCentroCoordinate[ownElementID])
            facesWeights = (np.dot(facesCf, facesUnitVector)
                            / (
                                    np.dot(facesCf, facesUnitVector) - np.dot(facesFf, facesUnitVector)
                            )
                            )
            self.facesWeights[facesID].append(float(facesWeights))
            self.facesCf[facesID].extend(list(facesCf))
            self.facesFf[facesID].extend(list(facesFf))
            self.facesCF[facesID].extend(list(facesCF))

        self.facesWallDist = [[] for _ in range(self.the_number_of_faces)]
        self.facesWallDistLimited = [[] for _ in range(self.the_number_of_faces)]
        for facesID in range(self.the_number_of_internalFaces, self.the_number_of_faces):
            facesUnitVector = np.array(self.facesSf[facesID]) / np.array(self.facesArea[facesID])
            ownElementID = self.facesID2ownerElementsID[facesID][0]
            facesCf = np.array(self.facesCentroCoordinate[facesID]) - np.array(
                self.elementsCentroCoordinate[ownElementID])
            facesCF = np.array(self.facesCentroCoordinate[facesID]) - np.array(
                self.elementsCentroCoordinate[ownElementID])
            facesWeights = 1
            facesWallDist = np.max((np.dot(facesCf, facesUnitVector), 1e-24))
            facesWallDistLimited = np.max((facesWallDist, 0.05 * np.sqrt(np.dot(facesCf, facesCf))))
            self.facesWeights[facesID].append(float(facesWeights))
            self.facesCf[facesID].extend(list(facesCf))
            self.facesCF[facesID].extend(list(facesCF))
            self.facesWallDist[facesID].append(float(facesWallDist))
            self.facesWallDistLimited[facesID].append(float(facesWallDistLimited))
    def __call__(self):
        self.calculate_the_number_of_boundaryElements()
        self.calculate_elementsID2neighbourElementsID()
        self.calculate_elementsID2facesID()
        self.calculate_elementsID2pointsID()
        self.calculate_upperAnbCoeffID_and_lowerAnbCoeffID()

        self.calculate_pointsID2elementsID()
        self.calculate_pointsID2facesID()

        self.calculate_facesCentroCoordinate_and_facesSf_and_facesArea()
        self.calculate_elementsCentroCoordinate_and_elementsVolume()
        self.calculate_facesWeights_and_facesWallDist_and_facesWallDistLimited()