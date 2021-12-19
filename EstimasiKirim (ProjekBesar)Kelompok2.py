# Aplikasi Estimasi Kirim
# Kelompok 3 (TI 2F)
# 1. Aditya Raihan Setyoputra (NIM. 2041720236)
# 2. Khairun Nisa             (NIM. 2041720188)
# 3. Nisrina Hasyimiyyah      (NIM. 2041720109)

# Import library
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
import tkinter
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Membuat root dan set title untuk GUI
root = Tk()
root.title('Estimasi Kirim')
root.resizable(width=False, height=False)

# Style font
styling = tkfont.Font(family='Tekton Pro', weight='bold', size=12)

# Pengaturan tinggi dan lebar dari GUI
HEIGHT = 400
WIDTH = 550
canvas = Canvas(root, height=HEIGHT, width=WIDTH, bg='#CCCCFF')
canvas.pack()

# Pilihan Hari Kirim
options = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu",
    "Minggu"
]

# Frame untuk judul aplikasi
frameJudul = Frame(root, bg='white')
frameJudul.place(rely=0.025,relx=0.5,relheight=0.1,relwidth=0.8,anchor='n')
judul = Label(frameJudul, bg='white',text=' Aplikasi Estimasi Kirim', font=styling)
judul.place(relheight=1,relwidth=1)

# Frame untuk input Jarak Kota
frameJarak = Frame(root, bg='white')
frameJarak.place(rely=0.2,relx=0.5,relheight=0.06,relwidth=0.8,anchor='n')
jarakKota = Label(frameJarak, bg='white',text='Jarak Kota')
jarakKota.place(relwidth=0.4,relheight=1)
jarakEntry = Entry(frameJarak)
jarakEntry.place(relx=0.4,relheight=1,relwidth=0.6)
jarakEntry.get()

# Frame untuk input Hari Kirim
frameHariKirim = Frame(root, bg='white')
frameHariKirim.place(rely=0.29,relx=0.5,relheight=0.06,relwidth=0.8,anchor='n')
harikirim = Label(frameHariKirim, bg='white',text='Hari Kirim')
harikirim.place(relwidth=0.4,relheight=1)
harikirimEntry = ttk.Combobox(frameHariKirim, value=options)
harikirimEntry.current(0)
harikirimEntry.place(relx=0.4,relheight=1,relwidth=0.6)
harikirimEntry.get()

# Frame untuk hasil Durasi Kirim
frameEstimasi = Frame(root, bg='white')
frameEstimasi.place(rely=0.38,relx=0.5,relheight=0.06,relwidth=0.8,anchor='n')
estimasi = Label(frameEstimasi, bg='white',text='Durasi Kirim')
estimasi.place(relwidth=0.4,relheight=1)

# Frame untuk hasil keterangan lama pengiriman
frameKeterangan = Frame(root, bg='white')
frameKeterangan.place(rely=0.47,relx=0.5,relheight=0.06,relwidth=0.8,anchor='n')
keterangan = Label(frameKeterangan, bg='white',text='Keterangan')
keterangan.place(relwidth=0.4,relheight=1)

# Fungsi untuk menentukan keterangan lama pengiriman
def durasistring(pencari):
    if(pencari <= 2):
        Kirim = 'Sangat Cepat'
    elif(pencari > 2 and pencari <= 4):
        Kirim = 'Cepat'
    elif(pencari > 4 and pencari <= 6):
        Kirim = 'Sedang'
    elif(pencari > 6 and pencari <= 8):
        Kirim = 'Lambat'
    else:
        Kirim = 'Sangat Lambat'
    return Kirim

# Fungsi untuk menentukan hasil durasi kirim menggunakan logika fuzzy
def proses():        
    # the universe of variables and membership function
    jarak = ctrl.Antecedent(np.arange(0, 5250, 1), 'jarak')
    kirim = ctrl.Antecedent(np.arange(0, 8, 1), 'kirim')
    durasi = ctrl.Consequent(np.arange(0, 11, 1), 'durasi')

    # Fungsi keanggotaan untuk masing-masing variabel
    # (jarak, kirim, dan durasi)
    # Rules
    jarak['sangat_dekat'] = fuzz.trimf(jarak.universe, [0, 400, 800.5])
    jarak['dekat'] = fuzz.trimf(jarak.universe, [801, 1100, 1500.5])
    jarak['sedang'] = fuzz.trimf(jarak.universe, [1501, 2000, 2500.5])
    jarak['jauh'] = fuzz.trimf(jarak.universe, [2501, 3000, 3500.5])
    jarak['sangat_jauh'] = fuzz.trimf(jarak.universe, [3501, 4375, 5250.5])

    kirim['weekday'] = fuzz.trimf(kirim.universe, [0, 2, 5.5])
    kirim['weekend'] = fuzz.trimf(kirim.universe, [5.5, 6, 7.5])

    durasi['sangat_cepat'] = fuzz.trimf(durasi.universe, [1, 1, 2.5])
    durasi['cepat'] = fuzz.trimf(durasi.universe, [2, 3, 4.5])
    durasi['sedang'] = fuzz.trimf(durasi.universe, [4, 5, 6.5])
    durasi['lambat'] = fuzz.trimf(durasi.universe, [6, 7, 8.5])
    durasi['sangat_lambat'] = fuzz.trimf(durasi.universe, [8, 9, 10])

    # Deklarasi rule
    rule1 = ctrl.Rule(jarak['sangat_dekat'] & kirim['weekday'], durasi['sangat_cepat'])
    rule2 = ctrl.Rule(jarak['sangat_dekat'] & kirim['weekend'], durasi['cepat'])
    rule3 = ctrl.Rule(jarak['dekat'] & kirim['weekday'], durasi['cepat'])
    rule4 = ctrl.Rule(jarak['dekat'] & kirim['weekend'], durasi['sedang'])
    rule5 = ctrl.Rule(jarak['sedang'] & kirim['weekday'], durasi['sedang'])
    rule6 = ctrl.Rule(jarak['sedang'] & kirim['weekend'], durasi['lambat'])
    rule7 = ctrl.Rule(jarak['jauh'] & kirim['weekday'], durasi['sedang'])
    rule8 = ctrl.Rule(jarak['jauh'] & kirim['weekend'], durasi['lambat'])
    rule9 = ctrl.Rule(jarak['sangat_jauh'] & kirim['weekday'], durasi['lambat'])
    rule10 = ctrl.Rule(jarak['sangat_jauh'] & kirim['weekend'], durasi['sangat_lambat'])

    durasi_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])

    braking = ctrl.ControlSystemSimulation(durasi_ctrl)

    # Pemilihan untuk convert hari kirim menjadi angka
    if(harikirimEntry.get() == options[0]):
        kirim = 1
    elif(harikirimEntry.get() == options[1]):
        kirim = 2
    elif(harikirimEntry.get() == options[2]):
        kirim = 3
    elif(harikirimEntry.get() == options[3]):
        kirim = 4
    elif(harikirimEntry.get() == options[4]):
        kirim = 5
    elif(harikirimEntry.get() == options[5]):
        kirim = 6
    elif(harikirimEntry.get() == options[6]):
        kirim = 7

    braking.input['jarak'] = int(jarakEntry.get())
    braking.input['kirim'] = kirim

    braking.compute()
    DurasiKirim = int(braking.output['durasi'])
    
    # Menampilkan hasil durasi kirim ke layar
    hasilEstimasi = Label(frameEstimasi, bg='white', text=str(DurasiKirim) + " Hari")
    hasilEstimasi.place(relx=0.4,relheight=1,relwidth=0.6)
    
    # Menampilkan hasil keterangan lama pengiriman ke layar
    hasilKeterangan = Label(frameKeterangan, bg='white',text=durasistring(DurasiKirim))
    hasilKeterangan.place(relx=0.4,relheight=1,relwidth=0.6)

# Fungsi untuk menghapus semua data yang diinputkan
def hapusData():
    jarakEntry.delete(0, tkinter.END)
    harikirimEntry.current(0)

    hasilEstimasi = Label(frameEstimasi, bg='white', text=" ")
    hasilEstimasi.place(relx=0.4,relheight=1,relwidth=0.6)

    hasilKeterangan = Label(frameKeterangan, bg='white',text=" ")
    hasilKeterangan.place(relx=0.4,relheight=1,relwidth=0.6)

# Frame untuk tombol Lihat Durasi dan Hapus Data
frameButton = Frame(root, bg='white')
frameButton.place(rely=0.62,relx=0.5,relheight=0.18,relwidth=0.24,anchor='n')
lihatdurasi = Button(frameButton, text='Lihat Durasi', command=proses)
lihatdurasi.place(rely=0,relx=0.5,relheight=0.5,relwidth=1,anchor='n')
hapusdata = Button(frameButton, text='Hapus Data', command=hapusData)
hapusdata.place(rely=0.5,relx=0.5,relheight=0.5,relwidth=1,anchor='n')

root.mainloop()