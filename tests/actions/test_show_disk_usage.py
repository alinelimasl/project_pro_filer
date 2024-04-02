import random
import pytest
from pro_filer.actions.main_actions import show_disk_usage  # NOQA
import os


@pytest.fixture
def context(tmp_path):
    test_dir = tmp_path / "src"
    test_dir.mkdir()

    file1 = test_dir / "app.py"
    file1.write_text("conteúdo do arquivo 1")

    file2 = test_dir / "__init__.py"
    file2.write_text("conteúdo do arquivo 2")

    total_size = sum(
        os.path.getsize(str(test_dir / file)) for file in [file1, file2]
    )

    all_files = [
        str(test_dir / "app.py"),
        str(test_dir / "__init__.py"),
    ]

    sorted_files = sorted(
        all_files, key=lambda x: os.path.getsize(x), reverse=True
    )

    return {
        "all_files": all_files,
        "total_size": total_size,
        "sorted_files": sorted_files,
    }


def test_show_disk_usage_with_files(context, capsys):
    show_disk_usage(context)
    captured = capsys.readouterr()
    assert f"Total size: {context['total_size']}" in captured.out
    assert "src/app.py" in captured.out
    assert "src/__init__.py" in captured.out


def test_show_disk_usage_without_files(capsys):
    context = {"all_files": []}
    show_disk_usage(context)
    captured = capsys.readouterr()
    assert captured.out == "Total size: 0\n"


def test_show_disk_usage_with_files_sorted(context, capsys):
    show_disk_usage(context)
    captured = capsys.readouterr()
    assert f"Total size: {context['total_size']}" in captured.out
    assert "src/app.py" in captured.out
    assert "src/__init__.py" in captured.out
    lines = captured.out.strip().split("\n")
    sizes = [
        int(line.split()[1]) for line in lines[:-1]
    ]  # Extract sizes from each line
    assert sizes == sorted(
        sizes, reverse=True
    )  # Check if sizes are sorted in descending order


def test_show_disk_usage_with_single_file(context, capsys):
    context = {
        "all_files": [context["all_files"][0]],
        "total_size": os.path.getsize(context["all_files"][0]),
    }
    show_disk_usage(context)
    captured = capsys.readouterr()
    assert f"Total size: {context['total_size']}" in captured.out
    assert "src/app.py" in captured.out
    assert "src/__init__.py" not in captured.out
    assert context["all_files"][0] not in captured.out


def test_show_disk_usage_with_unsorted_files(context, capsys):
    unsorted_files = context["all_files"][:]
    random.shuffle(unsorted_files)

    context = {
        "all_files": unsorted_files,
        "total_size": context["total_size"],
    }

    show_disk_usage(context)
    captured = capsys.readouterr()
    assert f"Total size: {context['total_size']}" in captured.out
    assert "src/app.py" in captured.out
    assert "src/__init__.py" in captured.out
    assert "src/app.py" in captured.out.splitlines()[0]
