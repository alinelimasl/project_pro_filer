from pro_filer.actions.main_actions import show_preview  # NOQA
import pytest


@pytest.fixture
def test_show_preview_with_files_and_dirs(capsys):
    context = {
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
        ],
        "all_dirs": ["src", "src/utils"],
    }
    show_preview(context)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Found 3 files and 2 directories\n"
        "First 5 files: ['src/__init__.py', 'src/app.py', "
        "'src/utils/__init__.py']\n"
        "First 5 directories: ['src', 'src/utils']\n"
    )


def test_show_preview_with_empty_files_and_dirs(capsys):
    context = {"all_files": [], "all_dirs": []}
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == "Found 0 files and 0 directories\n"


def test_show_preview_with_only_files(capsys):
    context = {
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
            "src/utils/helpers.py",
            "src/utils/constants.py",
        ],
        "all_dirs": [],
    }
    show_preview(context)
    captured = capsys.readouterr()
    expected_output = (
        "Found 5 files and 0 directories\n"
        "First 5 files: ['src/__init__.py', 'src/app.py', "
        "'src/utils/__init__.py', 'src/utils/helpers.py', "
        "'src/utils/constants.py']\n"
        "First 5 directories: []\n"
    )
    assert captured.out == expected_output


def test_show_preview_with_only_dirs(capsys):
    context = {
        "all_files": [],
        "all_dirs": [
            "src",
            "src/utils",
            "src/utils/tests",
            "src/utils/docs",
            "src/utils/config",
        ],
    }
    show_preview(context)
    captured = capsys.readouterr()
    expected_output = (
        "Found 0 files and 5 directories\n"
        "First 5 files: []\n"
        "First 5 directories: ['src', 'src/utils', 'src/utils/tests', "
        "'src/utils/docs', 'src/utils/config']\n"
    )
    assert captured.out == expected_output


def test_show_preview_with_more_than_5_files_and_dirs(capsys):
    context = {
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
            "src/utils/helpers.py",
            "src/utils/constants.py",
            "src/utils/tests/test_utils.py",
        ],
        "all_dirs": [
            "src",
            "src/utils",
            "src/utils/tests",
            "src/utils/docs",
            "src/utils/config",
            "src/utils/assets",
        ],
    }
    show_preview(context)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Found 6 files and 6 directories\n"
        "First 5 files: ['src/__init__.py', 'src/app.py', "
        "'src/utils/__init__.py', 'src/utils/helpers.py', "
        "'src/utils/constants.py']\n"
        "First 5 directories: ['src', 'src/utils', 'src/utils/tests', "
        "'src/utils/docs', 'src/utils/config']\n"
    )


if __name__ == "__main__":
    pytest.main([__file__])
