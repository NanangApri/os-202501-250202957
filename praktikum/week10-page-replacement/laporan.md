

# Laporan Praktikum Minggu 10
Topik: Manajemen Memori – Page Replacement (FIFO & LRU)

---

## Identitas
- **Nama**  : Nanang Apriyanto  
- **NIM**   : 250202957 
- **Kelas** : 1IKRA

---

## Tujuan
Tujuan praktikum minggu ini:  
> 1. Mahasiswa mampu mengimplementasikan algoritma page replacement FIFO dalam program.
> 2. Mahasiswa mampu mengimplementasikan algoritma page replacement LRU dalam program.
> 3. Mahasiswa mampu menjalankan simulasi page replacement dengan dataset tertentu.
> 4. Mahasiswa mampu membandingkan performa FIFO dan LRU berdasarkan jumlah page fault.
> 5. Mahasiswa mampu menyajikan hasil simulasi dalam laporan yang sistematis.
---

## Dasar Teori
Memori virtual merupakan mekanisme yang memungkinkan sistem operasi menyediakan ruang alamat logis yang lebih besar daripada kapasitas memori fisik. Mekanisme ini dicapai dengan membagi memori ke dalam unit halaman (page) yang dapat dipindahkan antara memori utama dan media penyimpanan sekunder.

Page fault terjadi ketika suatu proses mengakses halaman yang belum berada di memori utama. Pada kondisi ini, sistem operasi akan memuat halaman yang diperlukan dari penyimpanan sekunder ke dalam memori utama sebelum proses dapat dilanjutkan.

Algoritma FIFO (First-In First-Out) adalah algoritma page replacement yang mengganti halaman berdasarkan urutan waktu kedatangannya ke memori. Halaman yang pertama kali dimuat ke dalam memori akan menjadi halaman pertama yang dipilih untuk digantikan ketika diperlukan ruang memori baru.

Algoritma LRU (Least Recently Used) merupakan algoritma page replacement yang mengganti halaman berdasarkan waktu akses terakhir. Halaman yang paling lama tidak diakses akan dipilih untuk digantikan ketika terjadi page fault dan memori utama berada dalam kondisi penuh.

Algoritma page replacement berperan penting dalam mengelola penggunaan memori utama secara efisien. Pemilihan algoritma yang tepat dapat meminimalkan terjadinya page fault dan meningkatkan kinerja sistem secara keseluruhan.

---

## Langkah Praktikum
1. Langkah-langkah yang dilakukan.  

1.) **Menyiapkan Dataset**

   Gunakan *reference string* berikut sebagai contoh:
   ```
   7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2
   ```
   Jumlah frame memori: **3 frame**.

2.) **Implementasi FIFO**

   - Simulasikan penggantian halaman menggunakan algoritma FIFO.
   - Catat setiap *page hit* dan *page fault*.
   - Hitung total *page fault*.

3.) **Implementasi LRU**

   - Simulasikan penggantian halaman menggunakan algoritma LRU.
   - Catat setiap *page hit* dan *page fault*.
   - Hitung total *page fault*.


**(Keterangan: Di Minggu ini saya menggunakan bahasa pemrograman python di Visual Studio Code untuk mengimplementasikan Algoritma.)**

4.) Melakukan **Eksekusi & Validasi**

   - Jalankan program untuk FIFO dan LRU.
   - Pastikan hasil simulasi logis dan konsisten.
   - Simpan screenshot hasil eksekusi.

5.) Melakukan **Analisis Perbandingan**

   Membuat tabel perbandingan seperti berikut:

   | Algoritma | Jumlah Page Fault | Keterangan |
   |:--|:--:|:--|
   | FIFO | ... | ... |
   | LRU | ... | ... |


   - Jelaskan mengapa jumlah *page fault* bisa berbeda?
   - Analisis algoritma mana yang lebih efisien dan alasannya.

2. Perintah yang dijalankan. 
```bash
pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]

frame_size = 3


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


def fifo(pages, frame_size):
    frames = []         
    index_fifo = 0     
    faults = 0         
    hits = 0           
    rows = []          

    for step, page in enumerate(pages, start=1):

        if page in frames:
            status = "HIT"
            hits += 1

        else:
            status = "Fault"
            faults += 1

            if len(frames) < frame_size:
                frames.append(page)

            else:
                frames[index_fifo] = page
                index_fifo = (index_fifo + 1) % frame_size  

        show = frames + ["-"] * (frame_size - len(frames))

        rows.append({
            "step": step,
            "page": page,
            "f1": show[0],
            "f2": show[1],
            "f3": show[2],
            "status": status
        })

    print_table(rows, "=== SIMULASI ALGORITMA FIFO ===")
    print(f"Total Page HIT   = {hits}")
    print(f"Total Page FAULT = {faults}")
    return faults


def lru(pages, frame_size):
    frames = []         
    last_used = {}      # menyimpan kapan terakhir halaman dipakai
    faults = 0
    hits = 0
    rows = []

    for step, page in enumerate(pages, start=1):

        if page in frames:
            status = "HIT"
            hits += 1

        else:
            status = "Fault"
            faults += 1

            # jika frame belum penuh → langsung masuk
            if len(frames) < frame_size:
                frames.append(page)

            # jika frame penuh → cari halaman yang paling lama tidak dipakai
            else:
                lru_page = min(last_used, key=last_used.get)  
                frames[frames.index(lru_page)] = page         
                del last_used[lru_page]                       

        last_used[page] = step

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

print("PROGRAM SIMULASI PAGE REPLACEMENT: FIFO & LRU")
print("Reference String :", pages)
print("Jumlah Frame     :", frame_size)

fifo_faults = fifo(pages, frame_size)

lru_faults = lru(pages, frame_size)

print("\n=== HASIL ===")
print(f"Total Page Fault Algoritma FIFO : {fifo_faults}")
print(f"Total Page Fault Algoritma LRU  : {lru_faults}")

```
3. File dan kode yang dibuat. 

laporan.md, page_replacement.py, reference_string.txt, hasil_simulasi.png

4. Commit message yang digunakan. --> **Minggu 10 - Page Replacement FIFO & LRU**

---

## Kode / Perintah
Potongan kode atau perintah utama:
```bash

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

```

---

## Hasil Eksekusi
Screenshot hasil percobaan:
![Screenshot hasil](screenshots/hasil_simulasi.png)


**Eksekusi & Validasi**

   - Jalankan program untuk FIFO dan LRU. ✓
   - Pastikan hasil simulasi logis dan konsisten. ✓
   - Simpan screenshot hasil eksekusi. ✓

---

## Analisis
**Tabel Perbandingan**

   | Algoritma | Jumlah Page Fault | Keterangan |
   |:--|:--:|:--:|
   | FIFO | 10 | Mengganti halaman berdasarkan urutan kedatangan. Halaman yang paling awal masuk akan diganti lebih dulu ketika memori penuh. |
   | LRU | 9 | Mengganti halaman yang paling lama tidak digunakan berdasarkan waktu akses terakhir. |

- **Jelaskan mengapa jumlah *page fault* bisa berbeda?**

**Jawaban:** Terdapat beberapa faktor yang menyebabkan jumlah *page fault* bisa berbeda :

1. Algoritma page replacement yang digunakan -> 
Setiap algoritma memiliki strategi berbeda dalam memilih halaman yang diganti. FIFO mengganti halaman yang paling dulu masuk, sedangkan LRU mengganti halaman yang paling lama tidak dipakai. Perbedaan strategi ini membuat jumlah page fault yang dihasilkan bisa berbeda.

2. Urutan akses pada reference string ->
Jika halaman yang sama sering diakses berulang, maka page yang dibutuhkan sudah ada di memori sehingga page fault lebih sedikit. Namun jika urutan aksesnya banyak halaman baru, page fault akan lebih sering terjadi. Contohnya pada Pada FIFO, halaman yang paling dulu masuk akan diganti terlebih dahulu, sehingga jika urutan akses masih membutuhkan halaman lama, page fault bisa meningkat. Sedangkan pada LRU, halaman yang paling lama tidak dipakai yang diganti. Karena itu, jika ada banyak akses ulang terhadap halaman yang sama, LRU cenderung menghasilkan page fault lebih sedikit dibanding FIFO.

3. Jumlah frame yang tersedia
Semakin sedikit frame, semakin cepat memori penuh sehingga halaman lama lebih cepat tergantikan. Akibatnya page fault lebih sering muncul dibandingkan jika jumlah frame lebih banyak. Contohnya jika frame sedikit, FIFO lebih cepat mengganti halaman berdasarkan urutan masuk, sehingga halaman yang masih diperlukan bisa terganti. LRU tetap memilih halaman yang paling lama tidak dipakai, sehingga halaman yang sering digunakan lebih terjaga. Meski jumlah frame sama, strategi pemilihan ini membuat page fault FIFO dan LRU bisa berbeda.

- **Analisis algoritma mana yang lebih efisien dan alasannya.**

**Jawaban:**
Menurutku algorima yang lebih efisien adalah algoritma LRU, karena mengganti halaman yang paling lama tidak dipakai, sehingga meminimalkan page fault dan mengikuti pola penggunaan nyata program. Sedangkan algoritma FIFO hanya mengganti halaman berdasarkan urutan masuk, sehingga halaman yang masih sering dipakai bisa terbuang, membuat kinerjanya kurang efisien meski algoritmanya lebih sederhana dan mudah diimplementasikan.

---

## Kesimpulan
Berdasarkan hasil simulasi yang telah dilakukan, baik dengan algoritma FIFO maupun LRU, diperoleh jumlah page fault yang berbeda sesuai dengan strategi penggantian halaman masing-masing algoritma. 

Dari hasil pengujian, algoritma LRU menghasilkan jumlah page fault yang lebih sedikit dibandingkan FIFO pada dataset yang digunakan. Dengan demikian, dapat disimpulkan bahwa LRU lebih efisien karena mempertahankan halaman yang sering diakses, sedangkan FIFO mengganti halaman berdasarkan urutan masuk tanpa mempertimbangkan frekuensi penggunaan.

Simulasi ini membantu mempermudah pemahaman tentang pengaruh strategi penggantian halaman terhadap performa sistem. Hasilnya menekankan bahwa pemilihan algoritma page replacement yang tepat sangat penting untuk mengurangi page fault dan meningkatkan efisiensi penggunaan memori.

---

## Quiz
1. Apa perbedaan utama FIFO dan LRU?

**Jawaban:**

Perbedaan utama FIFO dan LRU terletak pada cara menentukan halaman yang akan diganti ketika memori berada dalam kondisi penuh.
FIFO mengganti halaman berdasarkan urutan kedatangan ke memori, sedangkan LRU mengganti halaman berdasarkan waktu akses terakhir, yaitu halaman yang paling lama tidak digunakan.

2. Mengapa FIFO dapat menghasilkan Belady’s Anomaly?

**Jawaban:**

FIFO dapat mengalami Belady’s Anomaly karena pemilihan halaman yang diganti hanya didasarkan pada urutan masuk ke memori, tanpa memperhatikan halaman tersebut masih sering digunakan atau tidak. Ketika jumlah frame memori ditambah, susunan halaman di dalam memori dapat berubah sehingga halaman yang penting justru tereliminasi lebih awal. Akibatnya, jumlah page fault pada kondisi tertentu dapat meningkat meskipun kapasitas memori diperbesar.

3. Mengapa LRU umumnya menghasilkan performa lebih baik dibanding FIFO? 

**Jawaban:**

Karena algoritma ini mempertimbangkan pola penggunaan halaman. LRU mempertahankan halaman yang baru saja digunakan dengan asumsi bahwa halaman tersebut kemungkinan besar akan diakses kembali dalam waktu dekat (locality of reference). Sebaliknya, FIFO hanya mengganti halaman berdasarkan urutan kedatangan tanpa melihat apakah halaman tersebut masih sering digunakan, sehingga berpotensi mengganti halaman yang masih dibutuhkan dan meningkatkan jumlah page fault. Semakin sedikit page fault, kinerja (performa) sistem menjadi lebih baik, sehingga LRU umumnya menghasilkan performa yang lebih baik dibanding FIFO.

---

## Refleksi Diri

- Apa bagian yang paling menantang minggu ini?  
Pada saat memahami materi tentang algoritma page replacement FIFO terutama algoritma page replacement LRU.
- Bagaimana cara Anda mengatasinya?  
Mencari serta mempelajari materi yang ingin di pelajari yaitu tentang algoritma FIFO dan Algoritma LRU di google dan youtube serta sumber/referensi yang terkait agar memperoleh pemahaman yang lebih jelas mengenai konsep algoritma FIFO dan algoritma LRU serta cara menerapkannya dalam bentuk kode program.


---

## Referensi
1. Silberschatz, A., Galvin, P., Gagne, G. *Operating System Concepts*, 10th Ed.
2. Tanenbaum, A. *Modern Operating Systems*, 4th Ed.
3. OSTEP – Virtual Memory & Page Replacement.
   
---

**Credit:**  
_Template laporan praktikum Sistem Operasi (SO-202501) – Universitas Putra Bangsa_
