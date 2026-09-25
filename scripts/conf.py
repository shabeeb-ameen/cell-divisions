import os
class conf:
    def __init__(self):
        self.run_dir = os.getcwd() + os.sep
        self.init_time = 0
        self.final_time = 10
        self.time_step = 0.005
        self.vtk_dump_freq = 10
        self.log_freq = 10
        self.s0 = 5.2
        self.gamma = 1
        self.Lth = 0.02
        self.temp = 1e-4
        self.kv = 10.
        self.box_size = 64
        self.fiber_ks = 10.0
        self.fiber_l0 = 2.8284271
        self.fiber_kb = 0.001
        self.link_N = 100
        self.link_k = 10.
        self.link_l0 = 1.5
        self.link_l1 = 0.2
        self.link_shrink_start_time = 1000
        self.link_shrink_speed = 0.004

    def write(self, filename="conf"):
        with open(self.run_dir + filename, "w") as file:
            file.write(f"time {self.init_time} {self.final_time} {self.time_step}\n")
            file.write(f"dump vtk {self.vtk_dump_freq}\n")
            file.write(f"log {self.log_freq}\n")
            file.write(f"s0 {self.s0} {self.gamma}\n")
            file.write(f"Lth {self.Lth}\n")
            file.write(f"T {self.temp}\n")
            file.write(f"kv {self.kv}\n")
            file.write(f"box {self.box_size:d} {self.box_size:d} {self.box_size:d} p p p\n")
            file.write(f"fiber {self.fiber_ks} {self.fiber_l0} {self.fiber_kb}\n")
            file.write(f"link {self.link_N} {self.link_k} {self.link_l0} {self.link_l1} {self.link_shrink_speed} {self.link_shrink_start_time}")


# def main():
#     conf().write()

# if __name__ == "__main__":
#     main()
