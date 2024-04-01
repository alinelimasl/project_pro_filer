from pro_filer.actions.main_actions import find_duplicate_files  # NOQA
import pytest


@pytest.fixture
def example_files(tmp_path):
    path_one_output = tmp_path / "folder1"
    path_two_output = tmp_path / "folder2"
    path_three_output = tmp_path / "file1.txt"
    path_one_output.mkdir()
    path_two_output.mkdir()
    path_three_output.touch()
    path_three_output.write_text("test content")
    example_text_one = path_one_output / "text1.txt"
    example_text_two = path_two_output / "text1.txt"
    example_text_one.touch()
    example_text_two.touch()
    return [
        str(example_text_one),
        str(example_text_two),
        str(path_three_output),
    ]


def test_different_exception_files():
    except_context = {"all_files": ["file1.py", "file2.py", "file3.py"]}
    with pytest.raises(ValueError):
        find_duplicate_files(except_context)


def test_different_duplicates_files(example_files):
    duplicated_context = {"all_files": example_files}
    resulted = find_duplicate_files(duplicated_context)
    assert len(resulted) == 1
    assert "text1.txt" in resulted[0][0]
    assert "text1.txt" in resulted[0][1]
