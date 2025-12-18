import time
import csv
import re

import solver

K = 25
SUBSETS = 10

def split_into_subsets(items, n_subsets=10):



    N = len(items)
    base = N // n_subsets
    extra = N % n_subsets

    subsets = []
    start = 0
    for i in range(n_subsets):
        size = base + (1 if i < extra else 0)
        subsets.append(items[start:start + size])
        start += size
    return subsets

def parse_costs(output_text: str):





    init_m = re.search(r"Init total cost:\s*([0-9.]+)", output_text)
    fin_m  = re.search(r"Final total cost:\s*([0-9.]+)", output_text)
    if not init_m or not fin_m:
        return None, None
    return float(init_m.group(1)), float(fin_m.group(1))

def main():

    warehouses, customers = solver.read_csv_input_data("locations.csv")
    warehouse = warehouses[0]

    print("Depo:", (warehouse.x, warehouse.y))
    print("Müşteri sayısı:", len(customers))

    subsets = split_into_subsets(customers, n_subsets=SUBSETS)
    for i, sub in enumerate(subsets, start=1):
        print(f"Subset {i}: {len(sub)} müşteri")

    rows = []
    for i, sub in enumerate(subsets, start=1):
        sub_copy = list(sub)
        print(f"\n=== SUBSET {i} ÇALIŞIYOR ({len(sub)} müşteri) ===")

        start_time = time.perf_counter()
        out_text = solver.solve_vrp(
            warehouses=[warehouse],
            customers=sub_copy,
            is_plot=False
        )
        elapsed = time.perf_counter() - start_time

        init_cost, final_cost = parse_costs(out_text)
        if init_cost is None:

            print("UYARI: Init/Final cost parse edilemedi. solver.py patch’ini yapman gerekiyor.")
            init_cost = float("nan")
            final_cost = float("nan")
            improvement = float("nan")
        else:
            improvement = (init_cost - final_cost) / init_cost * 100.0 if init_cost > 0 else 0.0

        rows.append({
            "Subset": i,
            "N": len(sub),
            "Init": init_cost,
            "Final": final_cost,
            "Imp (%)": improvement,
            "Time (s)": elapsed
        })

        print(f"Init: {init_cost:.6f} | Final: {final_cost:.6f} | Imp: {improvement:.2f}% | Time: {elapsed:.2f}s")


    out_path = "results_table.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Subset", "N", "Init", "Final", "Imp (%)", "Time (s)"])
        w.writeheader()
        w.writerows(rows)

    print("\nKaydedildi:", out_path)

if __name__ == "__main__":
    main()