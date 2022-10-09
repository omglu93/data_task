import os
import types
import pytest
import pandas as pd

from iso3166.utils import read_data, calculate_levenshtein_ratio,\
    export_to_parquet
from fixtures import generate_file_path, generate_folder_path,\
    generate_output_folder_path


def test_read_data_file(generate_file_path):

    data = read_data(generate_file_path)

    assert isinstance(data, types.GeneratorType)
    assert type(next(data)) == pd.DataFrame


def test_read_data_folder(generate_folder_path):

    data = read_data(generate_folder_path)

    assert isinstance(data, types.GeneratorType)
    assert type(next(data)) == pd.DataFrame
    assert type(next(data)) == pd.DataFrame


def test_read_data_file_exception_int():
    with pytest.raises(Exception) as e_info:
        data = read_data(12)


def test_read_data_file_exception_wrong_path():
    with pytest.raises(Exception) as e_info:
        data = read_data("/not/ok/path")


def test_read_data_folder_exception_int():
    with pytest.raises(Exception) as e_info:
        data = read_data(12)


def test_read_data_folder_exception_wrong_path():
    with pytest.raises(Exception) as e_info:
        data = read_data("/not/ok/path")


def test_levenshtein_calculation_perf_match():

    base = "Canada"
    target = "Canada"

    x = calculate_levenshtein_ratio(base, target)

    assert x == 1


def test_levenshtein_calculation_close_match():

    base = "Canaaada"
    target = "Canada"

    x = calculate_levenshtein_ratio(base, target)

    assert x >= 0.9


def test_levenshtein_calculation_no_match():

    base = "nothing"
    target = "Canada"

    x = calculate_levenshtein_ratio(base, target)

    assert x <= 0.5


def test_levenshtein_calculation_none_val():

    base = None
    target = "Canada"
    with pytest.raises(TypeError) as e_info:
        calculate_levenshtein_ratio(base, target)


def test_export_to_parquet(generate_output_folder_path):

    test_df = pd.DataFrame(
        {"messy_country": ["no single", "countries", "here"]})

    export_to_parquet(generate_output_folder_path, test_df)
    file_list = os.listdir(generate_output_folder_path)

    for f in file_list:
        os.remove(os.path.join(generate_output_folder_path, f))

    assert len(file_list) == 1


def test_export_to_parquet_more_files(generate_output_folder_path,
                                      generate_folder_path):

    data = read_data(generate_folder_path)

    for df in data:
        export_to_parquet(generate_output_folder_path, df)

    file_list = os.listdir(generate_output_folder_path)

    for f in file_list:
        os.remove(os.path.join(generate_output_folder_path, f))

    assert len(file_list) == 2


def test_export_to_parquet_bad_path():

    test_df = pd.DataFrame(
        {"messy_country": ["no single", "countries", "here"]})
    some_bad_path = "/path/not/ok"

    with pytest.raises(OSError) as err:
        export_to_parquet(some_bad_path, test_df)




