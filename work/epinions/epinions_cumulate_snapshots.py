from datetime import date

if __name__ == "__main__":
    # input_file
    epinions_dataset_path = r"..."
    # output_file
    filtered_dataset_out = r"..."

    to_date = lambda text: date(*(map(int, text.split("/"))))

    # YYYY/MM/DD
    start_date = to_date("2001/01/01")
    end_date = to_date("2001/12/31")

    with open(epinions_dataset_path) as in_file:
        with open(filtered_dataset_out, "w") as out_file:
            for line in in_file:
                *other_data, cur = line.split()
                cur_date = to_date(cur)
                if start_date <= cur_date <= end_date:
                    print(" ".join(other_data), cur, file=out_file)