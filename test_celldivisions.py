# This test script is designed to test the cell division functionality of the tissue simulation.
# It evaluates the post-division topology of a spheroid after randomly selected cell in the spheroid is divided.
# Then it runs the simulation with the updated topology and cell parameters.

from toolbox.cellDivision import cellDivision
from scripts.conf import conf
from test_random_cellParameters import copy_sample_init_files_to_run_dir, run
import os
import random
import numpy as np
import sys


def write_daughter_cellparameters(cell_divider:cellDivision, filename:str="cellParameters.input"):
    run_dir = cell_divider.sample.config_dir_
    with open(run_dir+filename, "w") as f:
        f.write("id v0 s0 kv\n")
        for cellID in cell_divider.daughterCellIDs:
            v0 = 0.5
            s0 = 5.2
            kv = 10
            f.write(f"{cellID} {v0} {s0} {kv}\n")
def edit_conf_time(run_dir:str, init_time:float, final_time:float):
    conf_instance = conf()
    conf_instance.run_dir = run_dir
    conf_instance.init_time = init_time
    conf_instance.final_time = final_time
    conf_instance.write()
def write_daughter_cell_vtks(cell_divider:cellDivision, timearray):
    for time in timearray:
        for cellID in cell_divider.daughterCellIDs:
            vtk_filename = f"cell_{cellID}.{time:07d}.vtk"
            cell_divider.sample.write_cell_collection_vtk(cells_array=[cellID], filename=vtk_filename)

def main(argv):
    division_time = 20
    project_dir = os.path.abspath(argv[1] if len(argv) == 2 else os.getcwd()) + os.sep
    os.makedirs(project_dir+"tests/",exist_ok=True)
    run_dir = project_dir+"tests/test_celldivisions/"
    copy_sample_init_files_to_run_dir(run_dir)

    # ////
    # Alternatively, you can use the initialize function to set up the run_dir using Docker 
    # This requires Docker to be installed and running.
    # ///

    # initialize(run_dir)
    # write_conf(run_dir)

    edit_conf_time(run_dir, init_time=0, final_time=division_time)
    
    # spheroid_filename = "sample.topo"
    ECM_filename = "ECM.topo"
    cellParameters_filename = "cellParameters.input"
    exec_dir = project_dir+"build/tvm"

    print("Running overdamped motion pre division")
    run(run_dir=run_dir,exec_dir=exec_dir,spheroid_filename="sample.topo", ECM_filename= ECM_filename, cellParameters_filename=cellParameters_filename)
    ## Now, cell division is performed on a randomly selected cell in the spheroid.

    cell_divider = cellDivision.from_spheroid_config(config_dir=run_dir, input_filename=f"{division_time:07d}.sample.topo")
    cellID_to_divide = random.choice([cellID for cellID, cell in cell_divider.sample.cells_.items() if cell.type_ and cell.is_surface_])
    cell_divider.set_motherCellID(cellID_to_divide)
    cell_divider.evaluatePostDivisionTopology()
    cell_divider.sample.write_topo(filename="sample_after_division.topo")
    write_daughter_cellparameters(cell_divider, filename=cellParameters_filename)
    edit_conf_time(run_dir, init_time=division_time, final_time=2*division_time)
    print("Running overdamped motion post division")
    run(run_dir=run_dir,exec_dir=exec_dir,spheroid_filename="sample_after_division.topo", ECM_filename= ECM_filename, cellParameters_filename=cellParameters_filename)
    write_daughter_cell_vtks(cell_divider, timearray=np.arange(division_time, 2*division_time+1, 10))
if __name__ == "__main__":
    main(sys.argv)
    