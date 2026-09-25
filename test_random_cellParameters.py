from toolbox.spheroid import Spheroid
from scripts.conf import conf
import os
import random
import subprocess
import sys


def initialize(run_dir):
    os.makedirs(run_dir, exist_ok=True)
    subprocess.run(
        ["docker", "run", "--platform", "linux/amd64", "-v", f"{os.path.abspath(run_dir)}:/data", "tvm-initialization"],
        cwd=run_dir,
        check=True,
    )

# def write_conf(project_dir, run_dir):
#     subprocess.run([sys.executable, f"{project_dir}scripts/conf.py"], cwd=run_dir, check=True)

def write_conf(run_dir):
    conf_instance = conf()
    conf_instance.run_dir = run_dir
    conf_instance.write()

def copy_sample_init_files_to_run_dir(run_dir):
    # Delete the run_dir if it exists, then create it and copy the sample_init files into it
    if os.path.exists(run_dir):
        subprocess.run(["rm", "-rf", run_dir], check=True)
    os.makedirs(run_dir)
    subprocess.run(["cp", "-r", "sample_init/.", run_dir], check=True)

def run(run_dir, exec_dir, spheroid_filename, ECM_filename, cellParameters_filename ):
    subprocess.run(
        [
            exec_dir,
            run_dir + spheroid_filename,
            run_dir + ECM_filename,
            run_dir + cellParameters_filename,
        ],
        cwd=run_dir,
        check=True,
    )
    
def write_random_cellparameters(spheroid: Spheroid, filename: str="cellParameters.input"):
    with open(spheroid.config_dir_+filename, "w") as f:
        f.write("id v0 s0 kv\n")
        for cellID,cell in spheroid.cells_.items():
            if cell.type_:
                v0 = random.uniform(0.8, 1.2)
                s0 = random.uniform(5,5.8)
                kv = random.uniform(8,12)
                f.write(f"{cellID} {v0} {s0} {kv}\n")

def main(argv):
    project_dir = os.path.abspath(argv[1] if len(argv) == 2 else os.getcwd()) + os.sep
    os.makedirs(project_dir+"tests/",exist_ok=True)
    run_dir = project_dir+"tests/test_random_cellParameters/"

    copy_sample_init_files_to_run_dir(run_dir)

    # ////
    # Alternatively, you can use the initialize function to set up the run_dir using Docker 
    # This requires Docker to be installed and running.
    # ///

    # initialize(run_dir)
    # write_conf(run_dir)

    spheroid_filename = "sample.topo"
    ECM_filename = "ECM.topo"
    cellParameters_filename = "cellParameters.input"
    exec_dir = project_dir+"build/tvm"
    spheroid = Spheroid.from_config(config_dir = run_dir, input_filename = spheroid_filename)
    write_random_cellparameters(spheroid)
    run(run_dir=run_dir,exec_dir=exec_dir,spheroid_filename=spheroid_filename, ECM_filename= ECM_filename, cellParameters_filename=cellParameters_filename)

if __name__ == "__main__":
    main(sys.argv)
    # run_again()
    