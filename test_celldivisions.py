from toolbox import tissue
from toolbox import topology
from toolbox import cellDivision
import os
import random
import numpy as np

def evaluatePostDivisionTopology(sample:tissue.Sample, cellID:int, division_axis:list):
    cell = sample.cells_[cellID]
    newVertices = {}
    newEdges = {}
    newPolygons = {}
    newCells = {}
    motherEdgeIDToDaughterEdgeIDs = {}
    motherPolygonIDToDaughterPolygonIDs = {}

    # Identify mother edges and mother polygons. Create intersection vertices on mother edges.
    for polygonID in cell.polygons_:
        for edgeID in sample.polygons_[polygonID].edges_:
            edge = sample.edges_[edgeID]
            v0 = sample.vertices_[edge.vertices_[0]].position_
            v1 = sample.vertices_[edge.vertices_[1]].position_
            t = np.dot(np.subtract(cell.center_,v0),division_axis)/np.dot(np.subtract(v1,v0),division_axis)
            if t>0 and t<1:
                sample.polygons_[polygonID].is_mother_ = True
                if not polygonID in motherPolygonIDToDaughterPolygonIDs:
                    motherPolygonIDToDaughterPolygonIDs[polygonID] = []
                if edgeID not in motherEdgeIDToDaughterEdgeIDs:
                    motherEdgeIDToDaughterEdgeIDs[edgeID] = []
                    new_vertex = topology.Vertex(id=np.max(list(sample.vertices_.keys()))+1+len(newVertices))
                    new_vertex.setPosition(np.add(v0,np.multiply(t,np.subtract(v1,v0))))
                    new_vertex.is_daughter_ = True
                    newVertices[new_vertex.id_] = new_vertex
                    sample.edges_[edgeID].is_mother_ = True
                    sample.edges_[edgeID].intersection_vertex_ = new_vertex.id_


    # Create new dividing edges for the dividing polygon. Add to newEdges.
    # Note:There are more daugher edges that are created in the next step.            
    for polygonID in motherPolygonIDToDaughterPolygonIDs:
        newDividingEdge = topology.Edge(id=np.max(list(sample.edges_.keys()))+1+len(newEdges))
        newDividingEdge.is_in_dividing_polygon_ = True
        newDividingEdge.mother_polygon_id_ = polygonID
        vertices = []
        for edgeID in sample.polygons_[polygonID].edges_:
            if sample.edges_[edgeID].is_mother_:
                vertices.append(sample.edges_[edgeID].intersection_vertex_)
        for vertexID in vertices:
            newDividingEdge.addVertex(vertexID)
        newEdges[newDividingEdge.id_] = newDividingEdge

    # Create daugher edges for the mother edges. Each mother edge is divided into two daughter edges.
    # Add these to newEdges.
    for edgeID in motherEdgeIDToDaughterEdgeIDs:
        motherEdgeIDToDaughterEdgeIDs[edgeID] = [np.max(list(sample.edges_.keys()))+1+len(newEdges),
                                                np.max(list(sample.edges_.keys()))+2+len(newEdges)]
        newDaughterEdge1 = topology.Edge(id = motherEdgeIDToDaughterEdgeIDs[edgeID][0])
        newDaughterEdge2 = topology.Edge(id = motherEdgeIDToDaughterEdgeIDs[edgeID][1])
        newDaughterEdge1.is_daughter_ = True
        newDaughterEdge2.is_daughter_ = True
        newDaughterEdge1.mother_id_ = edgeID
        newDaughterEdge2.mother_id_ = edgeID
        vertices1 = [sample.edges_[edgeID].vertices_[0],sample.edges_[edgeID].intersection_vertex_]
        vertices2 = [sample.edges_[edgeID].vertices_[1],sample.edges_[edgeID].intersection_vertex_]
        for vertexID in vertices1:
            newDaughterEdge1.addVertex(vertexID)
        for vertexID in vertices2:
            newDaughterEdge2.addVertex(vertexID)
        newEdges[newDaughterEdge1.id_] = newDaughterEdge1
        newEdges[newDaughterEdge2.id_] = newDaughterEdge2

    # Create new dividing polygon. Add the dividing edges. to this polygon.
    # Add to newPolygons.
    dividingPolygon = topology.Polygon(id=np.max(list(sample.polygons_.keys()))+1+len(newPolygons))
    dividingPolygon.is_dividing_polygon_ = True
    for edgeID,edge in newEdges.items():
        if edge.is_in_dividing_polygon_:
            dividingPolygon.addEdge(edgeID)     
    newPolygons[dividingPolygon.id_] = dividingPolygon               

    # For each mother polygon there should be two daughter polygons. Each daughter polygon
    # has the corresponding dividing edge, two daughter edges and the other edges of the mother polygon.
    for polygonID in motherPolygonIDToDaughterPolygonIDs:
        motherPolygonIDToDaughterPolygonIDs[polygonID] = [np.max(list(sample.polygons_.keys()))+1+len(newPolygons),
                                                        np.max(list(sample.polygons_.keys()))+2+len(newPolygons)]
        newDaughterPolygon1 = topology.Polygon(id = motherPolygonIDToDaughterPolygonIDs[polygonID][0])
        newDaughterPolygon2 = topology.Polygon(id = motherPolygonIDToDaughterPolygonIDs[polygonID][1])
        newDaughterPolygon1.is_daughter_ = True
        newDaughterPolygon2.is_daughter_ = True
        newDaughterPolygon1.mother_id_ = polygonID
        newDaughterPolygon2.mother_id_ = polygonID
        # Add the dividing edges to both daughter polygons.
        for edgeID,edge in newEdges.items():
            if edge.is_in_dividing_polygon_ and edge.mother_polygon_id_ == polygonID:
                newDaughterPolygon1.addEdge(edgeID)
                newDaughterPolygon2.addEdge(edgeID)
                break
        # Add the daughter edges to the corresponding daughter polygons.
        # newDaughterPolygon1 should be "above" the dividing polygon plane.
        for edgeID,edge in newEdges.items():
            if edge.is_daughter_ and edge.mother_id_ in sample.polygons_[polygonID].edges_:
                if np.dot(
                    np.subtract(
                        sample.vertices_[edge.vertices_[0]].position_,cell.center_),
                        division_axis) > 0:
                    newDaughterPolygon1.addEdge(edgeID)
                elif np.dot(
                    np.subtract(
                        sample.vertices_[edge.vertices_[0]].position_,cell.center_),
                        division_axis) < 0:
                    newDaughterPolygon2.addEdge(edgeID)
                else: 
                    print("Error: The non intersecting vertex of the daughter edge is on the dividing plane.")
        
        # add the other edges from the mother polygon to the corresponding daughter polygons.
        for edgeID in sample.polygons_[polygonID].edges_:
            if not sample.edges_[edgeID].is_mother_:
                if np.dot(
                    np.subtract(
                        sample.vertices_[sample.edges_[edgeID].vertices_[0]].position_,cell.center_),
                        division_axis) > 0:
                    newDaughterPolygon1.addEdge(edgeID)
                elif np.dot(
                    np.subtract(
                        sample.vertices_[sample.edges_[edgeID].vertices_[0]].position_,cell.center_),
                        division_axis) < 0:
                    newDaughterPolygon2.addEdge(edgeID)
                else: 
                    print("Error: One of the edge vertices in the mother polygon is on the dividing plane.")
        newPolygons[newDaughterPolygon1.id_] = newDaughterPolygon1
        newPolygons[newDaughterPolygon2.id_] = newDaughterPolygon2
    # Arrange polygon vertices for each polygon in newPolygons.
    for polygonID,polygon in newPolygons.items():
        tmp_vertices=[]
        for edgeID in polygon.edges_:
            if edgeID in newEdges:
                tmp_vertices.append(newEdges[edgeID].vertices_)
            if edgeID in sample.edges_:
                tmp_vertices.append(sample.edges_[edgeID].vertices_)
        polygon.vertices_ = sample.resolve_polygon_edge_connectivity(tmp_vertices)

    # two new daughter cells.
    newDaughterCell1 = topology.Cell(id=np.max(list(sample.cells_.keys()))+1)
    newDaughterCell2 = topology.Cell(id=np.max(list(sample.cells_.keys()))+2)

    for polygonID,polygon in newPolygons.items():
        # Add the dividing polygon to both daughter cells.
        if polygon.is_dividing_polygon_:
            newDaughterCell1.addPolygon(polygonID)
            newDaughterCell2.addPolygon(polygonID)
        # Add the daughter polygons to the corresponding daughter cells.    
        signSet = set()
        for vertexID in polygon.vertices_:
            if vertexID in newVertices:
                if newVertices[vertexID].is_daughter_:
                    continue
                signSet.add(np.sign(np.dot(np.subtract(newVertices[vertexID].position_,cell.center_),division_axis)))
            elif vertexID in sample.vertices_:
                if sample.vertices_[vertexID].is_daughter_:
                    continue
                signSet.add(np.sign(np.dot(np.subtract(sample.vertices_[vertexID].position_,cell.center_),division_axis)))
        if len(signSet) > 1:
            print("Error: The polygon has vertices on both sides of the dividing plane.")
        elif len(signSet) == 1:
            if signSet.pop() > 0:
                newDaughterCell1.addPolygon(polygonID)
            else:
                newDaughterCell2.addPolygon(polygonID)
    # Add the remaining polygons from the mother cell to the corresponding daughter cells.
    for polygonID in cell.polygons_:
        polygon = sample.polygons_[polygonID]
        if not polygon.is_mother_:
            signSet = set()
            for vertexID in polygon.vertices_:
                if vertexID in newVertices:
                    if newVertices[vertexID].is_daughter_:
                        continue
                    signSet.add(np.sign(np.dot(np.subtract(newVertices[vertexID].position_,cell.center_),division_axis)))
                elif vertexID in sample.vertices_:
                    if sample.vertices_[vertexID].is_daughter_:
                        continue
                    signSet.add(np.sign(np.dot(np.subtract(sample.vertices_[vertexID].position_,cell.center_),division_axis)))
            if len(signSet) > 1:
                print("Error: The polygon has vertices on both sides of the dividing plane.")
            elif len(signSet) == 1:
                if signSet.pop() > 0:
                    newDaughterCell1.addPolygon(polygonID)
                else:
                    newDaughterCell2.addPolygon(polygonID)

    newCells[newDaughterCell1.id_] = newDaughterCell1
    newCells[newDaughterCell2.id_] = newDaughterCell2

    # update the topology in the sample.

    sample.vertices_.update(newVertices)
    sample.edges_.update(newEdges)
    for edgeID in motherEdgeIDToDaughterEdgeIDs:
        del sample.edges_[edgeID]
    sample.polygons_.update(newPolygons)
    for polygonID in motherPolygonIDToDaughterPolygonIDs:
        del sample.polygons_[polygonID]
    for polygonID,polygon in sample.polygons_.items():
        rearrangePolygonVerticesFlag = False
        for edgeID in polygon.edges_:
            if edgeID in motherEdgeIDToDaughterEdgeIDs:
                rearrangePolygonVerticesFlag = True
                polygon.edges_.remove(edgeID)
                for daughterEdgeID in motherEdgeIDToDaughterEdgeIDs[edgeID]:
                    polygon.addEdge(daughterEdgeID)
        if rearrangePolygonVerticesFlag:
            tmp_vertices=[]
            for edgeID in polygon.edges_:
                if edgeID in sample.edges_:
                    tmp_vertices.append(sample.edges_[edgeID].vertices_)
            polygon.vertices_ = sample.resolve_polygon_edge_connectivity(tmp_vertices)
    sample.cells_.update(newCells)
    del sample.cells_[cell.id_]
    for cellID,cell in sample.cells_.items():
        for polygonID in cell.polygons_:
            if polygonID in motherPolygonIDToDaughterPolygonIDs:
                cell.polygons_.remove(polygonID)
                for daughterPolygonID in motherPolygonIDToDaughterPolygonIDs[polygonID]:
                    cell.addPolygon(daughterPolygonID)
    print("Daughter cell IDs: ", newDaughterCell1.id_, newDaughterCell2.id_)
    # dumpCellVtk(sample, newDaughterCell1.id_)
    # dumpCellVtk(sample, newDaughterCell2.id_)

    return sample

def initialize(dir):
    os.makedirs(dir, exist_ok=True)
    os.system(f"cd {dir} python ../scripts/conf.py && docker run --platform linux/amd64 -v $(pwd):/data tvm-initialization && python ../scripts/conf.py")
    
def run(dir):
    os.system(f"cd {dir} && ../build/tvm")
    
def write_random_cellparameters(spheroid: Spheroid, filename: str="cellParameters.input"):
    with open(spheroid.config_dir_+filename, "w") as f:
        f.write("id v0 s0 kv\n")
        for cellID,cell in spheroid.cells_.items():
            if cell.type_:
                v0 = random.uniform(0.8, 1.2)
                s0 = random.uniform(5,5.8)
                kv = random.uniform(8,12)
                f.write(f"{cellID} {v0} {s0} {kv}\n")

def divide_random_cell(spheroid: Spheroid):
    real_cell_IDs = [cellID for cellID,cell in spheroid.cells_.items() if cell.type_]
    cellID = random.choice(real_cell_IDs)

    # with open(spheroid.config_dir_ + "cellParameters.input", "w") as f:
    #     f.write("id v0 s0 kv\n")
    return cellDivision.evaluatePostDivisionTopology(spheroid,cellID)
    
def main():
    dir = "test_celldivisions/"
    if os.path.exists(dir):
        os.system(f"rm -rf {dir}")
    initialize(dir)
    spheroid = Spheroid.from_config(config_dir=dir)
    new_spheroid = divide_random_cell(spheroid)

    # write_random_cellparameters(spheroid)
    run(dir)

if __name__ == "__main__":
    main()
    