import re
import shlex
import sys
from pathlib import Path

import pytest

import imagecast.cli


def set_command(options):
    command = f'imagecast {options}'
    sys.argv = shlex.split(command)


def test_cli_version(capsys):
    """
    Invoke `imagecast --version`.
    """
    # Run command and capture output.
    set_command("--version")
    with pytest.raises(SystemExit):
        imagecast.cli.run()
    captured = capsys.readouterr()

    # Verify output.
    assert re.match(r"imagecast [\d.]+", captured.out)


def test_cli_unsplash_converge(tmp_path, caplog):
    """
    Verify image management works.
    """
    output_file: Path = tmp_path / "imagecast-unsplash.png"
    set_command(f'--uri="https://unsplash.com/photos/WvdKljW55rM/download?force=true" --monochrome=80 --crop=850,1925,-950,-900 --width=640 --save="{output_file}" --debug')
    imagecast.cli.run()

    # Verify log output.
    assert "Starting new HTTPS connection (1): unsplash.com:443" in caplog.messages

    # Verify content output.
    payload = output_file.read_bytes()
    assert payload.startswith(b"\x89PNG\r\n\x1a\n\x00")


def test_cli_html_acquire(tmp_path, caplog):
    """
    Verify HTML DOM element acquisition works.
    """
    output_file: Path = tmp_path / "imagecast-iana-logo.png"
    set_command(f'--uri="https://www.iana.org/help/example-domains" --element="#logo" --save="{output_file}" --debug')
    imagecast.cli.run()

    # Verify log output.
    assert "Starting new HTTPS connection (1): www.iana.org:443" in caplog.messages

    # Verify content output.
    payload = output_file.read_bytes()
    assert payload.startswith(b"\x89PNG\r\n\x1a\n\x00")
