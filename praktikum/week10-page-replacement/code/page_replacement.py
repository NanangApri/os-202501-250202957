# ==========================================================
# PROGRAM SIMULASI PAGE REPLACEMENT: FIFO & LRU
# Reference String  : 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2
# Jumlah Frame      : 3
#
# Tujuan program:
# 1. Menunjukkan proses penggantian halaman (page replacement)
# 2. Menghitung Page Hit dan Page Fault
# 3. Membandingkan algoritma FIFO dan LRU
#
# Keterangan dasar:
# - Page Hit   : halaman yang diminta sudah ada di memori
# - Page Fault : halaman yang diminta belum ada di memori
# ==========================================================

# Daftar halaman yang akan diakses CPU (reference string)
pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]

# Jumlah frame (slot memori yang tersedia)
frame_size = 3


# ==========================================================
# FUNGSI CETAK TABEL
# Fungsi ini hanya bertugas mencetak hasil simulasi agar rapi
# (tanpa kolom keterangan)
# ==========================================================
def print_table(rows, title):
    line = "-" * 49  # garis pembatas
    print("\n" + title)
    print(line)
    print(f"| {'Step':^6} | {'Page':^6} | {'Frames':^15} | {'Status':^9} |")
    print(line)
    for r in rows:
        # gabungkan frame jadi format [a, b, c]
        frames_str = f"[{r['f1']}, {r['f2']}, {r['f3']}]"
        print(f"| {r['step']:^6} | {r['page']:^6} | {frames_str:^15} | {r['status']:^9} |")
    print(line)


# ==========================================================
# FIFO (First In First Out)
# Mengganti halaman yang MASUK PALING AWAL
# ==========================================================
def fifo(pages, frame_size):
    frames = []         # menyimpan halaman yang ada di frame
    index_fifo = 0      # pointer untuk menandai siapa yang paling awal masuk
    faults = 0          # penghitung page fault
    hits = 0            # penghitung page hit
    rows = []           # menyimpan data tiap step untuk ditampilkan

    # loop setiap halaman yang diakses
    for step, page in enumerate(pages, start=1):

        # --------- CEK APAKAH PAGE SUDAH ADA (HIT) ---------
        if page in frames:
            status = "HIT"
            hits += 1

        # --------- JIKA TIDAK ADA (FAULT) ---------
        else:
            status = "Fault"
            faults += 1

            # Jika frame masih kosong → langsung masukkan
            if len(frames) < frame_size:
                frames.append(page)

            # Jika frame sudah penuh → ganti halaman paling awal
            else:
                frames[index_fifo] = page
                index_fifo = (index_fifo + 1) % frame_size  # geser pointer FIFO

        # tampilkan isi frame (kalau belum penuh diisi tanda '-')
        show = frames + ["-"] * (frame_size - len(frames))

        rows.append({
            "step": step,
            "page": page,
            "f1": show[0],
            "f2": show[1],
            "f3": show[2],
            "status": status
        })

    # cetak tabel hasil simulasi
    print_table(rows, "=== SIMULASI ALGORITMA FIFO ===")
    print(f"Total Page HIT   = {hits}")
    print(f"Total Page FAULT = {faults}")
    return faults


# ==========================================================
# LRU (Least Recently Used)
# Mengganti halaman yang PALING LAMA TIDAK DIPAKAI
# ==========================================================
def lru(pages, frame_size):
    frames = []         # menyimpan halaman dalam frame
    last_used = {}      # menyimpan kapan terakhir halaman dipakai
    faults = 0
    hits = 0
    rows = []

    for step, page in enumerate(pages, start=1):

        # --------- HIT ---------
        if page in frames:
            status = "HIT"
            hits += 1

        # --------- FAULT ---------
        else:
            status = "Fault"
            faults += 1

            # jika frame belum penuh → langsung masuk
            if len(frames) < frame_size:
                frames.append(page)

            # jika frame penuh → cari halaman yang paling lama tidak dipakai
            else:
                lru_page = min(last_used, key=last_used.get)  # halaman LRU
                frames[frames.index(lru_page)] = page         # ganti halaman
                del last_used[lru_page]                       # hapus dari catatan

        # update kapan halaman terakhir dipakai
        last_used[page] = step

        # isi '-' bila frame belum penuh
        show = frames + ["-"] * (frame_size - len(frames))

        rows.append({
            "step": step,
            "page": page,
            "f1": show[0],
            "f2": show[1],
            "f3": show[2],
            "status": status
        })

    print_table(rows, "=== SIMULASI ALGORITMA LRU ===")
    print(f"Total Page HIT   = {hits}")
    print(f"Total Page FAULT = {faults}")
    return faults


# ==========================================================
# MAIN PROGRAM
# ==========================================================
print("PROGRAM SIMULASI PAGE REPLACEMENT: FIFO & LRU")
print("Reference String :", pages)
print("Jumlah Frame     :", frame_size)

# jalankan FIFO
fifo_faults = fifo(pages, frame_size)

# jalankan LRU
lru_faults = lru(pages, frame_size)

# tampilkan ringkasan
print("\n=== HASIL ===")
print(f"Total Page Fault Algoritma FIFO : {fifo_faults}")
print(f"Total Page Fault Algoritma LRU  : {lru_faults}")
