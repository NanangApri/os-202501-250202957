processes = {
    "P1": {"allocation": "R1", "request": "R2"},
    "P2": {"allocation": "R2", "request": "R3"},
    "P3": {"allocation": "R3", "request": "R1"}
}

def line():
    print("+----------+---------------+---------------+")

print("\nTabel Dataset")
line()
print("| Proses   | Allocation    | Request       |")
line()
for p, d in processes.items():
    print(f"| {p:<8} | {d['allocation']:<13} | {d['request']:<13} |")
line()

wait_for = {
    p1: [p2 for p2 in processes if processes[p1]["request"] == processes[p2]["allocation"]]
    for p1 in processes
}

print("\nTabel Proses yang Saling Menunggu")
print("+----------+---------------------------+")
print("| Proses   | Menunggu Proses           |")
print("+----------+---------------------------+")
for p, w in wait_for.items():
    print(f"| {p:<8} | {', '.join(w) if w else '-':<25} |")
print("+----------+---------------------------+")

def detect_deadlock(graph):
    visited, stack, deadlock = set(), [], set()

    def dfs(n):
        if n in stack:
            deadlock.update(stack[stack.index(n):])
            return
        if n in visited:
            return
        visited.add(n)
        stack.append(n)
        for x in graph.get(n, []):
            dfs(x)
        stack.pop()

    for n in graph:
        dfs(n)
    return deadlock

deadlock = detect_deadlock(wait_for)

print("\nTabel Hasil Deteksi Deadlock")
print("+----------+----------------------+")
print("| Proses   | Status               |")
print("+----------+----------------------+")
for p in processes:
    print(f"| {p:<8} | {'Deadlock' if p in deadlock else 'Tidak Deadlock':<20} |")
print("+----------+----------------------+")

print("\nKESIMPULAN")
print("-" * 40)
if deadlock:
    print("Sistem berada dalam kondisi deadlock.")
    print("Proses yang terlibat deadlock adalah:", ", ".join(deadlock))
else:
    print("Sistem tidak berada dalam kondisi deadlock.")