def main():
    init_time = 0
    final_time = 10
    time_step = 0.005
    vtk_dump_freq = 10
    log_freq = 10
    s0 = 5.2
    gamma = 1
    Lth = 0.02
    T = 1e-4
    kv = 10.
    box_size = 64
    fiber_ks = 10.0
    fiber_l0 = 2.8284271
    fiber_kb = 0.001
    link_N = 100
    link_k = 10.
    link_l0 = 1.5
    link_l1 = 0.2
    link_shrink_start_time = 1000
    link_shrink_speed = 0.004
    with open("conf", "w") as file:
        file.write(f"time {init_time} {final_time} {time_step}\n")
        file.write(f"dump vtk {vtk_dump_freq}\n")
        file.write(f"log {log_freq}\n")
        file.write(f"s0 {s0} {gamma}\n")
        file.write(f"Lth {Lth}\n")
        file.write(f"T {T}\n")
        file.write(f"kv {kv}\n")
        file.write(f"box {box_size:d} {box_size:d} {box_size:d} p p p\n")
        file.write(f"fiber {fiber_ks} {fiber_l0} {fiber_kb}\n")
        file.write(f"link {link_N} {link_k} {link_l0} {link_l1} {link_shrink_speed} {link_shrink_start_time}")

if __name__ == "__main__":
    main()
