"""Smoke tests for the CLI interface."""

import os
import tempfile
from pathlib import Path
from subprocess import run, PIPE

import pytest

# Create a temporary forbidden words file for testing
@pytest.fixture
def forbidden_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("obviously\nclearly\njust\nsimply\n")
    yield f.name
    os.unlink(f.name)

def test_cli_help():
    """Test that --help works."""
    res = run(
        ["python", "-m", "doc_agent", "--help"],
        text=True, stdout=PIPE, stderr=PIPE
    )
    assert res.returncode == 0
    assert "usage:" in res.stdout
    assert "doc-agent" in res.stdout

def test_cli_generate_smoke(forbidden_file):
    """Basic smoke test for the generate command."""
    res = run(
        [
            "python", "-m", "doc_agent",
            "generate",
            "--scenario", "Write a hello world function",
            "--style", "Friendly",
            "--forbidden-file", forbidden_file,
            "--fast"  # Use only fast evaluators for smoke test
        ],
        text=True, stdout=PIPE, stderr=PIPE
    )
    assert res.returncode == 0
    assert "✨ Final Text ✨" in res.stdout

def test_cli_process_smoke(forbidden_file, tmp_path):
    """Basic smoke test for the process command."""
    # Create a temporary Python file to process
    test_file = tmp_path / "test.py"
    test_file.write_text("""
def hello():
    '''
    A simple function.
    '''
    print("Hello, world!")
    """)
    
    res = run(
        [
            "python", "-m", "doc_agent",
            "process",
            str(test_file),
            "--forbidden-file", forbidden_file
        ],
        text=True, stdout=PIPE, stderr=PIPE
    )
    assert res.returncode == 0

def test_cli_invalid_command():
    """Test behavior with invalid command."""
    res = run(
        ["python", "-m", "doc_agent", "invalid"],
        text=True, stdout=PIPE, stderr=PIPE
    )
    assert res.returncode != 0

def test_cli_generate_json_output(forbidden_file):
    """Test JSON output format."""
    res = run(
        [
            "python", "-m", "doc_agent",
            "generate",
            "--scenario", "Write a greeting function",
            "--style", "Brief",
            "--forbidden-file", forbidden_file,
            "--fast",
            "--json"
        ],
        text=True, stdout=PIPE, stderr=PIPE
    )
    assert res.returncode == 0
    assert '"status":' in res.stdout  # Basic JSON structure check 