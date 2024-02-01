# Indonesian SMK Information Scraping

## Dataframe Columns

| Name | Description |
| ---- | ----------- |
| link | Link of the SMK profile page |
| npsn | Nomor Pokok Sekolah Nasional (National School Identification Number) |
| name | Name of the SMK |
| address | Full address of the SMK (no postal code) |
| akreditasi | Accreditation grade |
| kepala_sekolah | Headmaster / Principal |
| operator | Operator |
| guru | Total number of teachers |
| siswa_l | Number of male students |
| siswa_p | Number of female students |
| rombongan_belajar | Total number of study groups |
| kurikulum | Curriculum |
| penyelenggaraan | Operating times |
| mbs | Manajemen Berbasis Sekolah (School-Based Management) |
| semester_data | Semester data |
| akses_internet | Internet access |
| sumber_listrik | Electricity source |
| daya_listrik | Electrical power |
| luas_tanah_m2 | Area in square meters |
| ruang_kelas | Number of classrooms |
| laboratorium | Number of laboratories |
| perpustakaan | Number of libraries |
| sanitasi_siswa | Number of student sanitation |
| r_siswa_rombel | Ratio of students to study group |
| r_siswa_ruang_kelas | Ratio of students to classrooms | 
| r_siswa_guru | Ratio of students to teachers |
| p_guru_kualifikasi | Percentage of qualified teachers |
| p_guru_sertifikasi | Percentage of certified teachers | 
| p_guru_pns | Percentage of teachers who are civil servants |
| p_ruang_kelas_layak | Percentage of classrooms in acceptable condition |
| guru_status_pns | Number of teachers who are civil servants |
| guru_status_gtt | Number of part-time teachers | 
| guru_status_gty | Number of full-time teachers |
| guru_status_honor | Number of contract (honorer) teachers |
| guru_sertifikasi | Number of certified teachers |
| guru_belum_sertifikasi | Number of uncertified teachers |
| guru_ijazah_kurang_dari_S1 | Number of teachers with education less than bachelor degree |
| guru_ijazah_S1_atau_lebih | Number of teachers with bachelor degrees or higher |
| guru_ijazah_data_kosong | Number of teachers with missing education data |
| guru_jk_laki_laki | Number of male teachers |
| guru_jk_perempuan | Number of female teachers |
| tk_status_pns | Number of staff who are civil servants |
| tk_status_honor | Number of contract (honorer) staff |
| tk_total | Total number of staff |
| tk_ijazah_kurang_dari_S1 | Number of staff with education less than bachelor degree |
| tk_ijazah_S1_atau_lebih | Number of staff with bachelor degrees or higher |
| tk_ijazah_data_kosong | Number of staff with missing education data |
| tk_jk_laki_laki | Number of male staff |
| tk_jk_perempuan | Number of female staff |
| nilai_akreditasi_tahun | Year of accreditation |
| nilai_akreditasi_akhir | Last accreditation score (out of 100) |

## How to run
1. Setup a virtual environment by runnning `python -m venv .venv`
2. Install the packages listed in `requirements.txt`
3. Run the main file using `python run.py`