import random
from toolbox import tissue
from toolbox.spheroid import Spheroid
from toolbox import cellDivision

def main():
    sample = Spheroid(configDir = "samples/", simulationTime = 500, tissueType = "spheroid")
    isSurface = True
    cellType = 0
    while isSurface or cellType != 0:
        cellID = random.choice(list(sample.cells_.keys()))
        isSurface = sample.cells_[cellID].isSurface_
        cellType = sample.cells_[cellID].type_
    sample.cells_[cellID].is_mother_ = True
    print("Mother cell ID: ", cellID)
    cellDivision.dumpCellVtk(sample, cellID)
    sample = cellDivision.evaluatePostDivisionTopology(sample, cellID)
    cellDivision.dumpSample(sample)
    return

if __name__ == "__main__":
    main()