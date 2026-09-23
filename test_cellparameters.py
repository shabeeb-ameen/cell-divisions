from toolbox.spheroid import Spheroid
import os
import random
import subprocess

def initialize( dir ):
    os.makedirs(dir, exist_ok=True)
    os.system(f"cd {dir} python ../scripts/conf.py && docker run --platform linux/amd64 -v $(pwd):/data tvm-initialization && python ../scripts/conf.py")
    
def run(run_dir, exec_dir, spheroid_filename, ECM_filename, cellParameters_filename ):
    # subprocess.call([f"cd {run_dir} && {exec_dir}", f"{run_dir+spheroid_filename} {run_dir+ECM_filename} {run_dir + cellParameters_filename}"])

    os.system(f"cd {run_dir} && {exec_dir} {run_dir+spheroid_filename} {run_dir+ECM_filename} {run_dir + cellParameters_filename}")
    
def write_random_cellparameters(spheroid: Spheroid, filename: str="cellParameters.input"):
    with open(spheroid.config_dir_+filename, "w") as f:
        f.write("id v0 s0 kv\n")
        for cellID,cell in spheroid.cells_.items():
            if cell.type_:
                v0 = random.uniform(0.8, 1.2)
                s0 = random.uniform(5,5.8)
                kv = random.uniform(8,12)
                f.write(f"{cellID} {v0} {s0} {kv}\n")

def main():
    run_dir = "/Users/shabeebameen/Projects/3DVM-ECM/test_cellparameters/"
    # if os.path.exists(run_dir):
    #     os.system(f"rm -rf {run_dir}")
    # initialize(dir)
    spheroid_filename = "sample.topo"
    ECM_filename = "ECM.topo"
    cellParameters_filename = "cellParameters.input"
    exec_dir = "/Users/shabeebameen/Projects/3DVM-ECM/build/tvm"
    spheroid = Spheroid.from_config(config_dir=run_dir, input_filename=spheroid_filename)
    write_random_cellparameters(spheroid)
    run(run_dir=run_dir,exec_dir=exec_dir,spheroid_filename=spheroid_filename, ECM_filename= ECM_filename, cellParameters_filename=cellParameters_filename)

def run_again():
    run_dir = "/Users/shabeebameen/Projects/3DVM-ECM/test_cellparameters/"
    # if os.path.exists(run_dir):
    #     os.system(f"rm -rf {run_dir}")
    # initialize(dir)
    init_time = 10
    spheroid_filename = f"{init_time:07d}.sample.topo"
    ECM_filename = f"{init_time:07d}.ECM.topo"
    cellParameters_filename = "cellParameters.input"
    exec_dir = "/Users/shabeebameen/Projects/3DVM-ECM/build/tvm"
    # spheroid = Spheroid.from_config(config_dir=run_dir, input_filename=spheroid_filename)
    # write_random_cellparameters(spheroid)
    run(run_dir=run_dir,exec_dir=exec_dir,spheroid_filename=spheroid_filename, ECM_filename= ECM_filename, cellParameters_filename=cellParameters_filename)

if __name__ == "__main__":
    # main()
    run_again()
    