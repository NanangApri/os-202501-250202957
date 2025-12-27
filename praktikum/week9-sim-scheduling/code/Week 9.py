# ------------------------------------------------------------------------------------------------------------------------------------------------------
# CPU Scheduling: FCFS & SJF Non-Preemptive
# Program ini digunakan untuk menghitung Waiting Time dan Turnaround Time berdasarkan dua algoritma penjadwalan CPU, yaitu FCFS dan SJF Non-Preemptive.
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Dataset proses yang digunakan dalam simulasi
processes = [
    {"name": "P1", "arrival": 0, "burst": 6},
    {"name": "P2", "arrival": 1, "burst": 8},
    {"name": "P3", "arrival": 2, "burst": 7},
    {"name": "P4", "arrival": 3, "burst": 3},
]


# ------------------------------------------------------------
# Fungsi untuk menampilkan hasil perhitungan dalam bentuk tabel
# ------------------------------------------------------------
def print_table(results):
    line = "-" * 112
    print(line)
    print(f"| {'Proses':^8} | {'Arrival Time':^13} | {'Burst Time':^11} | {'Start Time':^11} | {'Finish Time':^12} | {'Waiting Time':^13} | {'Turnaround Time':^16} |")
    print(line)
    for r in results:
        print(f"| {r['name']:^8} | {r['arrival']:^13} | {r['burst']:^11} | {r['start']:^11} | {r['finish']:^12} | {r['waiting']:^13} | {r['turn']:^16} |")
    print(line)


# ------------------------------------------------------------
# Algoritma FCFS (First Come First Served)
# Proses dieksekusi berdasarkan urutan kedatangan
# ------------------------------------------------------------
def fcfs(processes):

    # Proses diurutkan berdasarkan arrival time
    procs = sorted(processes, key=lambda x: x["arrival"])

    current_time = 0
    results = []
    total_wait = total_turn = 0

    # Perhitungan dilakukan untuk setiap proses
    for p in procs:

        # Proses mulai dieksekusi ketika CPU sudah idle
        start = max(current_time, p["arrival"])

        # Waktu selesai adalah waktu mulai + burst time
        finish = start + p["burst"]

        # Waiting time = waktu mulai - waktu kedatangan
        waiting = start - p["arrival"]

        # Turnaround time = waktu selesai - waktu kedatangan
        turn = finish - p["arrival"]

        # Menyimpan hasil dalam list
        results.append({
            "name": p["name"], "arrival": p["arrival"], "burst": p["burst"],
            "start": start, "finish": finish, "waiting": waiting, "turn": turn
        })

        # Akumulasi total waktu
        total_wait += waiting
        total_turn += turn

        # Waktu CPU berpindah ke waktu selesai proses
        current_time = finish

    # Hasil diurutkan kembali berdasarkan waktu mulai proses
    results.sort(key=lambda x: x["start"])

    # Menampilkan tabel hasil
    print("\n=== FCFS ===")
    print_table(results)

    # Menghitung nilai rata-rata
    n = len(results)
    print(f"Rata-rata Waiting Time    = {total_wait/n}")
    print(f"Rata-rata Turnaround Time = {total_turn/n}")


# ------------------------------------------------------------------------------
# Algoritma SJF Non-Preemptive
# Proses dipilih berdasarkan burst time terkecil dari proses yang sudah datang.
# ------------------------------------------------------------------------------
def sjf(processes):

    # Menggunakan salinan list agar data asli tidak berubah
    procs = [p.copy() for p in processes]
    n = len(procs)

    completed = 0
    current_time = 0
    results = []
    total_wait = total_turn = 0

    # Loop berjalan hingga seluruh proses selesai dieksekusi
    while completed < n:

        # Menentukan proses yang sudah datang dan belum selesai
        ready = [p for p in procs if not p.get("done") and p["arrival"] <= current_time]

        # Jika belum ada proses yang datang,
        # maka waktu sistem akan maju
        if not ready:
            current_time += 1
            continue

        # Memilih proses dengan burst time terkecil
        p = min(ready, key=lambda x: x["burst"])

        # Menentukan waktu mulai proses
        start = max(current_time, p["arrival"])

        # Menentukan waktu selesai
        finish = start + p["burst"]

        # Waiting time = start - arrival
        waiting = start - p["arrival"]

        # Turnaround time = finish - arrival
        turn = finish - p["arrival"]

        # Menyimpan hasil perhitungan
        results.append({
            "name": p["name"], "arrival": p["arrival"], "burst": p["burst"],
            "start": start, "finish": finish, "waiting": waiting, "turn": turn
        })

        # Menambahkan ke total perhitungan
        total_wait += waiting
        total_turn += turn

        # Memperbarui waktu sistem dan status proses
        current_time = finish
        p["done"] = True
        completed += 1

    # Hasil akhir diurutkan berdasarkan waktu mulai eksekusi
    results.sort(key=lambda x: x["start"])

    # Menampilkan tabel hasil
    print("\n=== SJF Non-Preemptive ===")
    print_table(results)

    # Menampilkan rata-rata
    print(f"Rata-rata Waiting Time    = {total_wait/n}")
    print(f"Rata-rata Turnaround Time = {total_turn/n}")


# -------------------------------------------------------------------------------------------------------------------------------
# Bagian Utama Program (Main Program)
# Pada bagian ini pengguna diminta memilih algoritma penjadwalan yang akan digunakan, yaitu FCFS atau SJF Non-Preemptive.
# Setelah pilihan dimasukkan, program akan memanggil fungsi sesuai algoritma yang dipilih dan menampilkan hasil perhitungan. 
# -------------------------------------------------------------------------------------------------------------------------------
print("Pilih Algoritma:")
print("1. FCFS")
print("2. SJF Non-Preemptive")

choice = input("Masukkan pilihan (1/2): ")

if choice == "1":
    fcfs(processes)
elif choice == "2":
    sjf(processes)
else:
    print("Pilihan tidak valid.")