# This test script is designed to test the cell division functionality of the tissue simulation.
# It evaluates the post-division topology of a spheroid after randomly selected cell in the spheroid is divided.
# Then it runs the simulation with the updated topology and cell parameters.

from toolbox.spheroid import Spheroid
from toolbox.cellDivision import evaluatePostDivisionTopology
from scripts.conf import conf
from test_random_cellParameters import copy_sample_init_files_to_run_dir, run
import os
import random
import numpy as np
import sys
import json


def write_daughter_cellparameters(run_dir,daugthter_cells_list):
    with open(run_dir+"cellParameters.input", "w") as f:
        f.write("id v0 s0 kv\n")
        for cellID in daugthter_cells_list:
            v0 = 0.5
            s0 = 5.2
            kv = 10
            f.write(f"{cellID} {v0} {s0} {kv}\n")

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

    conf_instance = conf()
    conf_instance.run_dir = run_dir
    conf_instance.init_time = 0
    conf_instance.final_time = division_time
    conf_instance.write()
    # spheroid_filename = "sample.topo"
    ECM_filename = "ECM.topo"
    cellParameters_filename = "cellParameters.input"
    exec_dir = project_dir+"build/tvm"

    print("Running overdamped motion pre division")
    run(run_dir=run_dir,exec_dir=exec_dir,spheroid_filename="sample.topo", ECM_filename= ECM_filename, cellParameters_filename=cellParameters_filename)

    spheroid = Spheroid.from_config(config_dir=run_dir, input_filename=f"{division_time:07d}.sample.topo")
    cellID = random.choice([cellID for cellID, cell in spheroid.cells_.items() if cell.type_])
    spheroid_after_division, daughterCells = evaluatePostDivisionTopology(spheroid, cellID=cellID, division_axis=[1,0,0])
    spheroid_after_division.write_topo(filename="sample_after_division.topo")
    write_daughter_cellparameters(run_dir, daughterCells)
    conf_instance.init_time = division_time
    conf_instance.final_time = division_time + 20
    conf_instance.write()
    print("Running overdamped motion post division")
    run(run_dir=run_dir,exec_dir=exec_dir,spheroid_filename="sample_after_division.topo", ECM_filename= ECM_filename, cellParameters_filename=cellParameters_filename)

if __name__ == "__main__":
    main(sys.argv)
    