from pro_filer.actions.main_actions import show_details  # NOQA
from datetime import date


def test_show_details(capsys, tmp_path):
    file_path = tmp_path / "Trybe_logo.png"
    file_path.write_text("This is a test file")

    context = {"base_path": str(file_path)}

    show_details(context)

    captured = capsys.readouterr()
    last_modified_date = date.fromtimestamp(
        file_path.stat().st_mtime
    ).isoformat()
    expected_output = (
        f"File name: Trybe_logo.png\n"
        f"File size in bytes: {file_path.stat().st_size}\n"
        f"File type: file\n"
        f"File extension: .png\n"
        f"Last modified date: {last_modified_date}\n"
    )
    assert captured.out == expected_output


def test_show_details_directory(capsys):
    context = {"base_path": "/home/trybe/????"}
    show_details(context)

    captured = capsys.readouterr()
    assert captured.out == "File '????' does not exist\n"


def test_show_details_extension(capsys, tmp_path):
    file_path = tmp_path / "Trybe_logo"
    file_path.write_text("This is a test file")

    context = {"base_path": str(file_path)}

    show_details(context)

    captured = capsys.readouterr()
    last_modified_date = date.fromtimestamp(
        file_path.stat().st_mtime
    ).isoformat()

    assert "File name: Trybe_logo" in captured.out
    assert f"File size in bytes: {file_path.stat().st_size}" in captured.out
    assert "File type: file" in captured.out
    assert "File extension: [no extension]" in captured.out
    assert f"Last modified date: {last_modified_date}" in captured.out
