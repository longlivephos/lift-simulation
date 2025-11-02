# lantai_max            = lantai tertinggi yang bisa dicapai lift (dari input awal atau jumlah lantai maksimum)
# MAX_penumpang         = kapasitas maksimum penumpang lift
# MAX_berat             = kapasitas berat maksimum lift (kg)
# lantai_saat_ini       = posisi lift saat ini
# arah                  = arah gerak lift saat ini ("up" / "down")
# penumpang             = daftar penumpang yang ada di lift saat ini berisi tujuan dan berat
# daftar_tunggu         = daftar panggilan dari luar lift berisi arah dan lantai
# turun                 = penumpang yang harus turun di lantai saat ini
# panggilan_searah      = filter panggilan dari daftar_tunggu yang searah dengan arah lift saat ini
# penumpang_lolos       = penumpang yang baru naik di lantai saat ini dan lolos cek berat/kapasitas
# total_berat           = total berat penumpang di lift saat ini + penumpang baru
# total_penumpang       = total penumpang di lift saat ini + penumpang baru
# penumpang_naik        = jumlah penumpang yang berhasil naik lift pada satu panggilan
# panggilan_terproses   = daftar panggilan dari daftar_tunggu yang sudah diproses pada lantai saat ini



import time
lantai_atas = 4
MAX_penumpang = 13
MAX_berat = 1100
lantai_saat_ini = 1
arah = "up"
penumpang = []
daftar_tunggu = []

print("=== SELAMAT DATANG DI LIFT GKU 1 ITB! ===")
print("Masukkan data panggilan dari luar ('tidak' untuk lanjut)\n")

# user input panggilan luar
while True:
    panggilan = input("Apakah ada panggilan lift? (ya/tidak): ").lower()
    if panggilan == "tidak":
        break
    lantai = int(input("Masukkan lantai panggilan (1-4): "))
    arah_panggilan = input("Masukkan arah panggilan (up/down): ").lower()
    daftar_tunggu.append({"lantai": lantai, "arah": arah_panggilan})

print("\n=== Panggilan awal tersimpan ===")
for p in daftar_tunggu:
    print(f"Lantai {p['lantai']} memanggil lift untuk arah {p['arah']}")
print("================================\n")

# loop utama lift 
while True:
    # menampilkan status
    print("\n----------------------------------------")
    print(f"Lift saat ini di lantai {lantai_saat_ini} dengan arah: {arah.upper()}")
    print("----------------------------------------\n")
    time.sleep(1)

    # cek penumpang turun
    turun = [p for p in penumpang if p["tujuan"] == lantai_saat_ini]
    if turun:
        print(f"Lift berhenti di lantai {lantai_saat_ini} — {len(turun)} penumpang keluar.\n")
        for p in turun:
            penumpang.remove(p)

    # lantai tertinggi & terendah yang perlu dicapai (sebelum panggilan baru)
    semua_lantai = [p['lantai'] for p in daftar_tunggu] + [p['tujuan'] for p in penumpang]
    lantai_max = max(semua_lantai, default=1)
    lantai_min = min(semua_lantai, default=1)

    # sebelum lift berhenti, tanya panggilan baru
    while True:
        tambah_lagi = input("Apakah ada panggilan baru dari luar lift? (ya/tidak): ").lower()
        if tambah_lagi == "tidak":
            break
        elif tambah_lagi == "ya":
            lantai = int(input("Masukkan lantai panggilan (1-4): "))
            arah_panggilan = input("Masukkan arah panggilan (up/down): ").lower()
            daftar_tunggu.append({"lantai": lantai, "arah": arah_panggilan})
            print("\n=== Panggilan terbaru tersimpan ===")
            for p in daftar_tunggu:
                print(f"Lantai {p['lantai']} memanggil lift untuk arah {p['arah']}")
            print("================================\n")
        else:
            print("Input tidak valid. Masukkan 'ya' atau 'tidak'.")

    # cek penumpang naik
    panggilan_searah = [p for p in daftar_tunggu if p["lantai"] == lantai_saat_ini and p["arah"] == arah]
    penumpang_baru = []

    if panggilan_searah:
        print(f"Ada panggilan searah di lantai {lantai_saat_ini}. Penumpang masuk.\n")
        daftar_tunggu = [p for p in daftar_tunggu if p not in panggilan_searah]

        jumlah_penumpang = int(input("Masukkan jumlah penumpang yang masuk: "))
        total_berat = sum(p["berat"] for p in penumpang)
        total_penumpang = len(penumpang)

        for i in range(jumlah_penumpang):
            print(f"Penumpang {i+1}:")
            berat = float(input("   Berat penumpang (kg): "))
            tujuan = int(input("   Lantai tujuan (1-4): "))

            if total_berat + berat > MAX_berat or total_penumpang + 1 > MAX_penumpang:
                print(f"Penumpang {i+1} terlalu berat atau lift penuh, tunggu lift selanjutnya.\n")
                continue
            else:
                penumpang_baru.append({"tujuan": tujuan, "berat": berat})
                total_berat += berat
                total_penumpang += 1

    if penumpang_baru:
        penumpang.extend(penumpang_baru)
        print(f"{len(penumpang_baru)} penumpang naik ke lift.\n")

    # lantai tertinggi & terendah yang perlu dicapai jika daftar tunggu ditambah
    semua_lantai = [p['lantai'] for p in daftar_tunggu] + [p['tujuan'] for p in penumpang]
    if semua_lantai:
        lantai_max = max(semua_lantai)
        lantai_min = min(semua_lantai)
    else:
        print("Tidak ada daftar tunggu maupun penumpang tersisa. Lift berhenti.\n")
        break

    # pergerakan lift
    if arah == "up":
        if lantai_saat_ini < lantai_max:
            lantai_saat_ini += 1
            print(f"Lift naik ke lantai {lantai_saat_ini}...\n")
        else:
            if semua_lantai:
                arah = "down"
                print("Lift berbalik arah ke bawah.\n")
            else:
                print("Tidak ada daftar tunggu maupun penumpang tersisa. Lift berhenti.\n")
                break

    elif arah == "down":
        if lantai_saat_ini > lantai_min:
            lantai_saat_ini -= 1
            print(f"Lift turun ke lantai {lantai_saat_ini}...\n")
        else:
            if semua_lantai:
                arah = "up"
                print("Lift berbalik arah ke atas.\n")
            else:
                print("Tidak ada daftar tunggu maupun penumpang tersisa. Lift berhenti.\n")
                break

print("=== SELESAI ===")
