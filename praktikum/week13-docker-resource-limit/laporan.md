
# Laporan Praktikum Minggu 13
Topik: Docker – Resource Limit (CPU & Memori)

---

## Identitas
- **Nama**  : Nanang Apriyanto  
- **NIM**   : 250202957  
- **Kelas** : 1IKRA

---

## Tujuan
Tujuan praktikum minggu ini:  
> 1. Mahasiswa mampu menulis Dockerfile sederhana untuk sebuah aplikasi/skrip.
> 2. Mahasiswa mampu membangun image dan menjalankan container.
> 3. Mahasiswa mampu menjalankan container dengan pembatasan **CPU** dan **memori**.
> 4. Mahasiswa mampu mengamati dan menjelaskan perbedaan eksekusi container dengan dan tanpa limit resource.
> 5. Mahasiswa mampu menyusun laporan praktikum secara runtut dan sistematis.

---

## Dasar Teori
Docker adalah teknologi containerization yang menjalankan aplikasi dalam lingkungan terisolasi dengan memanfaatkan fitur kernel Linux seperti namespaces. Mekanisme ini membuat proses di dalam container terpisah secara logis dari sistem host dan container lainnya, meskipun masih menggunakan kernel yang sama.

Pembatasan penggunaan resource pada Docker dilakukan menggunakan Control Groups (cgroups). Cgroups memungkinkan sistem operasi mengatur dan membatasi pemakaian resource seperti CPU dan memori oleh container, sehingga setiap container hanya menggunakan resource sesuai batas yang ditentukan.

Pembatasan CPU mengatur porsi waktu CPU yang dapat digunakan oleh container, sehingga eksekusi program tetap berjalan namun dengan kecepatan yang disesuaikan. Sementara itu, pembatasan memori menetapkan batas maksimum memori, dan jika batas tersebut terlampaui, sistem dapat menghentikan proses melalui mekanisme Out Of Memory (OOM).

---

## Langkah Praktikum
1. Langkah-langkah yang dilakukan.
    
1.) **Persiapan Lingkungan**

   - Pastikan Docker terpasang dan berjalan.
   - Verifikasi:
     ```bash
     docker version
     docker ps
     ```

2.) **Membuat Aplikasi/Skrip Uji**

   Program sederhana di folder `code/` (bahasa Python) yang:
   - Melakukan komputasi berulang (untuk mengamati limit CPU), dan/atau
   - Mengalokasikan memori bertahap (untuk mengamati limit memori).

3.) **Membuat Dockerfile**

   - Tulis `Dockerfile` untuk menjalankan program uji.
   - Build image:
     ```bash
     docker build -t week13-resource-limit .
     ```

4.) **Menjalankan Container Tanpa Limit**

   - Jalankan container normal:
     ```bash
     docker run --rm week13-resource-limit
     ```
   - Catat output/hasil pengamatan.

5.) **Menjalankan Container Dengan Limit Resource**

   Jalankan container dengan batasan resource (contoh):
   ```bash
   docker run --rm --cpus="0.5" --memory="256m" week13-resource-limit
   ```
   Catat perubahan perilaku program (mis. lebih lambat, error saat memori tidak cukup, dll.).

6.) **Monitoring Sederhana**

   - Jalankan container (tanpa `--rm` jika perlu) dan amati penggunaan resource:
     ```bash
     docker stats
     ```
   - Ambil screenshot output eksekusi dan/atau `docker stats`. 

7.)  Melakukan commit ketika sudah selesai.

2. Perintah yang dijalankan. 

```bash
import os
import time

print(f"Process ID: {os.getpid()}")
print("Pengujian alokasi memori Docker.... \n", flush=True)

buffer = []

def get_real_memory_mb():
    try:
        with open("/sys/fs/cgroup/memory.current", "r") as f:
            return int(f.read()) // (1024 * 1024)
    except:
        return -1

while True:
    buffer.append("M" * 10_000_000)  # ±10 MB
    real_mb = get_real_memory_mb()
    print(f"Memori aktual container: {real_mb} MB", flush=True)
    time.sleep(0.5)
```
3. File dan kode yang dibuat.  
laporan.md, Dockerfile, app.py, hasil_limit.png, hasil_tidak_limit.png, Docker_version.png, Docker_ps.png, Build_image.png, hasil_limit_200m.png, Docker_Stats.png
4. Commit message yang digunakan. -> ** Minggu 13 - Docker Resource Limit **

---

## Kode / Perintah
Potongan kode atau perintah utama:

Dockerfile:
```bash
FROM python:3.15.0a3
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

app.py :
```bash
import os
import time

print(f"Process ID: {os.getpid()}")
print("Pengujian alokasi memori Docker.... \n", flush=True)

buffer = []

def get_real_memory_mb():
    try:
        with open("/sys/fs/cgroup/memory.current", "r") as f:
            return int(f.read()) // (1024 * 1024)
    except:
        return -1

while True:
    buffer.append("M" * 10_000_000)  # ±10 MB
    real_mb = get_real_memory_mb()
    print(f"Memori aktual container: {real_mb} MB", flush=True)
    time.sleep(0.5)
```

---

## Hasil Eksekusi
Screenshot hasil percobaan:

![Screenshot hasil](screenshots/Docker_version.png)
![Screenshot hasil](screenshots/Docker_ps.png)
![Screenshot hasil](screenshots/Build_image.png)
![Screenshot hasil](screenshots/hasil_limit.png)
![Screenshot hasil](screenshots/hasil_limit_200m.png)
![Screenshot hasil](screenshots/hasil_tidak_limit.png)
![Screenshot hasil](screenshots/Docker_Stats.png)



---

## Analisis
- **Tabel Hasil Pengamatan Pengujian Penggunaan Memori Container Docker**

| No | Aspek yang Diamati      | Hasil Pengamatan                             |
| -- | ----------------------- | -------------------------------------------- |
| 1  | Status awal container   | Container berhasil dijalankan tanpa kendala  |
| 2  | Penggunaan memori awal  | 13 MB                                |
| 3  | Pola penggunaan memori  | Mengalami peningkatan secara bertahap        |
| 4  | Kondisi operasional     | Container tetap berjalan stabil              |
| 5  | Penghentian pengujian   | Proses dihentikan secara paksa oleh pengguna |
| 6  | Penggunaan memori akhir | 692 MB                               |
| 7  | Kesalahan sistem        | Tidak ditemukan kesalahan selama pengujian   |

Menjalankan container tanpa limit sumber daya berarti container tidak diberikan batasan penggunaan memori oleh Docker. Akibatnya, container dapat menggunakan memori sistem secara bebas sesuai kebutuhan proses yang berjalan di dalamnya. Pada pengujian ini, penggunaan memori meningkat secara bertahap selama container dijalankan dan tidak terjadi penghentian otomatis oleh sistem. Pengujian dihentikan secara paksa oleh pengguna, sehingga penggunaan memori akhir bukan merupakan batas maksimum container. Kondisi ini menunjukkan bahwa tanpa pengaturan limit, container berpotensi mengonsumsi sumber daya sistem dalam jumlah besar.

- **Tabel Hasil Pengamatan Pengujian Container dengan Batasan Resource**

| No | Aspek yang Diamati     | Hasil Pengamatan                                                   |
| -- | ---------------------- | ------------------------------------------------------------------ |
| 1  | Konfigurasi resource   | CPU dibatasi sebesar 0,5 core dan memori dibatasi                  |
| 2  | Penggunaan memori awal | Penggunaan memori meningkat secara bertahap                        |
| 3  | Batas memori 256 MB (Simulasi 1)   | Penggunaan memori berhenti pada kisaran ±255 MB                    |
| 4  | Batas memori 200 MB (Simulasi 2)   | Penggunaan memori berhenti pada kisaran ±199 MB                    |
| 5  | Perilaku program       | Program tidak dapat menambah alokasi memori setelah mencapai batas |
| 6  | Kondisi container      | Container tetap berjalan stabil tanpa mengalami crash              |
| 7  | Error sistem           | Tidak ditemukan error Out of Memory                                |
| 8  | Penghentian pengujian  | Proses dihentikan secara manual oleh pengguna                      |

Pada pengujian ini, saya melakukan dua simulasi Menjalankan Container Dengan Limit Resource dengan penerapan batasan (limit) resource pada container Docker. Simulasi pertama menggunakan batas memori sebesar 256 MB, sedangkan simulasi kedua menggunakan batas memori sebesar 200 MB, dengan pembatasan CPU sebesar 0,5 core pada kedua skenario. Hasil pengujian menunjukkan bahwa penggunaan memori pada masing-masing simulasi meningkat hingga mendekati nilai batas yang ditetapkan, kemudian tidak dapat bertambah lebih lanjut. Hal ini membuktikan bahwa mekanisme pembatasan resource pada Docker berjalan sesuai dengan konfigurasi yang diterapkan.


- **Tabel Hasil Pengamatan Monitoring Resource Menggunakan docker stats**

| No | Skenario Pengujian            | CPU Usage | Memori  | Persentase Memori | Keterangan                            |
| -- | ----------------------------- | --------- | ---------------------- | ----------------- | ------------------------------------- |
| 1  | Container tanpa limit         | ±0,94%    | 692,2 MB / 7,64 GB     | ±8,84%            | Memori dapat digunakan secara bebas   |
| 2  | Container dengan limit 256 MB | ±2,25%    | 255,9 MB / 256 MB      | ±99,96%           | Memori mencapai batas yang ditetapkan |
| 3  | Container dengan limit 200 MB | ±2,43%    | 199,9 MB / 200 MB      | ±99,97%           | Memori mencapai batas yang ditetapkan |

Monitoring menggunakan perintah docker stats menunjukkan adanya perbedaan antara container tanpa batasan resource dan container dengan penerapan batasan memori. Pada container tanpa limit, penggunaan memori berada pada tingkat yang relatif rendah jika dibandingkan dengan total kapasitas memori sistem yang tersedia. Sebaliknya, pada container yang dibatasi dengan memori sebesar 256 MB dan 200 MB, tingkat penggunaan memori mencapai hampir seluruh batas yang telah ditetapkan. Hasil ini menunjukkan bahwa perintah docker stats efektif digunakan sebagai alat pemantauan penggunaan resource container secara real-time sekaligus sebagai sarana verifikasi terhadap penerapan mekanisme pembatasan resource pada Docker.

---

## Kesimpulan
Berdasarkan hasil praktikum, penggunaan resource pada container Docker dapat dikendalikan dengan baik melalui pengaturan batas CPU dan memori. Container yang dijalankan tanpa limit cenderung menggunakan memori secara bebas, sedangkan container dengan limit hanya menggunakan resource sesuai batas yang ditentukan.

Penerapan batas memori(limit) menunjukkan bahwa Docker mampu membatasi alokasi memori tanpa menyebabkan container berhenti secara tiba-tiba. Hal ini membantu menjaga kestabilan sistem ketika menjalankan aplikasi yang berpotensi menggunakan memori dalam jumlah besar.

Pemantauan menggunakan perintah docker stats memudahkan pengamatan penggunaan resource secara langsung dan membantu memahami perbedaan perilaku container dengan dan tanpa pembatasan resource.


---

## Quiz
1. Mengapa container perlu dibatasi CPU dan memori?  
   **Jawaban:**  
   Container perlu dibatasi CPU dan memori karena Docker menjalankan container di atas sistem host yang sama dan memanfaatkan Control Groups (cgroups) untuk mengatur alokasi resource. Pembatasan ini mencegah satu container menggunakan resource secara berlebihan sehingga tidak mengganggu container lain maupun kestabilan sistem host.

   Selain itu, dalam teori manajemen resource sistem operasi, pembatasan resource bertujuan untuk menjamin keadilan, efisiensi, dan isolasi antar proses. Dengan membatasi CPU dan memori, sistem operasi dapat melakukan resource sharing secara terkendali serta mencegah kegagalan sistem akibat kehabisan memori.

2. Apa perbedaan VM dan container dalam konteks isolasi resource?  
   **Jawaban:**  Perbedaan antara VM dan container dalam konteks isolasi resource terletak pada tingkat virtualisasi dan mekanisme isolasi yang digunakan. Virtual Machine (VM) menyediakan isolasi yang kuat, karena setiap VM menjalankan OS sendiri di atas hypervisor, jadi CPU dan memori dialokasikan terpisah secara penuh dari sistem host maupun VM lain.


   Sebaliknya, container berbagi kernel sistem operasi host dan mengandalkan mekanisme kernel seperti namespaces dan control groups (cgroups) untuk isolasi dan pembatasan resource. Membuat container lebih ringan, efisien, tapi tingkat isolasinya tidak sekuat VM. Dikarenakan semuanya masih nyambung ke kernel yang sama,. Jadi, meskipun efisien, ada risiko kalau kernel bermasalah, semua container bisa kena akibatnya. 


3. Apa dampak limit memori terhadap aplikasi yang boros memori?  
   **Jawaban:** Pembatasan memori memberikan dampak signifikan terhadap aplikasi yang memiliki penggunaan memori tinggi. Aplikasi hanya diperbolehkan menggunakan memori hingga batas yang telah ditetapkan, sehingga ketika kebutuhan memori aplikasi melebihi batas tersebut, sistem operasi akan menghentikan proses melalui mekanisme Out Of Memory (OOM).

   Kondisi ini dapat menyebabkan aplikasi gagal berjalan atau berhenti secara paksa. Namun, pembatasan memori diperlukan untuk menjaga kestabilan sistem serta mencegah satu aplikasi mengonsumsi memori secara berlebihan yang dapat mengganggu aplikasi lain maupun sistem host. 

---

## Refleksi Diri
Tuliskan secara singkat:
- Apa bagian yang paling menantang minggu ini? Pada saat Membuat bahasa program serta menjalankan container dengan Limit Resource.
- Bagaimana cara Anda mengatasinya? 
Mempelajari kembali sintaks Python dan penggunaan perintah Docker untuk pembatasan resource, serta melakukan percobaan berulang hingga container dapat berjalan sesuai konfigurasi.


---

## Referensi
1. Docker Documentation – Resource constraints (CPU/Memory).  
2. Linux Kernel Docs – Control Groups (cgroups) dan namespaces.  
3. OSTEP – Virtualization / Resource Management.

---

**Credit:**  
_Template laporan praktikum Sistem Operasi (SO-202501) – Universitas Putra Bangsa_
