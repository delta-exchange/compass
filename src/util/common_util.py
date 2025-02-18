def get_report_index(total_records, batch_size):
    index = total_records // batch_size + 1
    if index <= 9:
        return f"0{index}"
    return f"{index}"
