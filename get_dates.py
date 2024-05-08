import csv

def read_from_csv(filename):
    rows = []
    with open(filename, newline='\n') as file:
        rd = csv.reader(file)
        header = next(rd)
        for row in rd:
            rows.append(row)
    return header, rows

def read_ids():
    files = ["csv/missing_npsn_dates/missing_SMA.csv",
             "csv/missing_npsn_dates/missing_SMK.csv"]
    _, rows_SMA = read_from_csv(files[0])
    _, rows_SMK = read_from_csv(files[1])
    rows = rows_SMA + rows_SMK
    return rows