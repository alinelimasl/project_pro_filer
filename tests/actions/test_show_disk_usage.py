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

    total_size = sum(os.path.getsize(file) for file in [file1, file2])

    return {
        "all_files": [
            "app.py",
            "__init__.py",
        ],
        "total_size": total_size,
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
