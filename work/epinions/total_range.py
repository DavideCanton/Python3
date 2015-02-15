__author__ = 'Kami'

from datetime import date

if __name__ == "__main__":
    dataset_path = r"U:\home\kami\Documenti\Ext_Epinions\user_rating.txt"

    to_date = lambda text: date(*(map(int, text.split("/"))))

    # YYYY/MM/DD
    max_date = to_date("1/1/1")
    min_date = to_date("6000/12/31")

    with open(dataset_path) as file_in:
        for line in file_in:
            *_, cur = line.split()
            cur_date = to_date(cur)
            min_date = min(min_date, cur_date)
            max_date = max(max_date, cur_date)

    print(min_date)
    print(max_date)
