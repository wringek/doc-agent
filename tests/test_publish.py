import pytest
from pathlib import Path
from doc_agent.publish import write_doc

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir

def test_write_doc_basic(tmp_path, monkeypatch):
    """Test basic document generation with minimal sections."""
    # Mock the output directory to use a temporary path
    monkeypatch.chdir(tmp_path)
    
    sections = {
        "summary": "A test function that does testing."
    }
    
    write_doc(sections, "test_function")
    
    # Check that the file was created
    doc_path = tmp_path / "output" / "test_function.md"
    assert doc_path.exists()
    
    # Check content
    content = doc_path.read_text()
    assert "# test_function" in content  # Title is the filename
    assert "A test function that does testing." in content

def test_write_doc_all_sections(tmp_path, monkeypatch):
    """Test document generation with all possible sections."""
    monkeypatch.chdir(tmp_path)
    
    sections = {
        "summary": "A complete test function.",
        "purpose": "Used for testing all sections.",
        "usage": "import test_function",
        "arguments": "arg1: str - first argument",
        "returns": "bool - success status",
        "examples": "test_function('example')"
    }
    
    write_doc(sections, "complete_function")
    
    # Check content
    content = (tmp_path / "output" / "complete_function.md").read_text()
    
    # Verify all sections are present
    assert "# complete_function" in content  # Title is the filename
    assert "A complete test function." in content
    assert "## Purpose" in content
    assert "Used for testing all sections." in content
    assert "## Usage" in content
    assert "## Arguments" in content
    assert "## Returns" in content
    assert "## Examples" in content

def test_write_doc_empty_sections(tmp_path, monkeypatch):
    """Test that empty sections are skipped."""
    monkeypatch.chdir(tmp_path)
    
    sections = {
        "summary": "A minimal function.",
        "purpose": "",  # Empty section
        "examples": "  "  # Whitespace-only section
    }
    
    write_doc(sections, "minimal_function")
    
    content = (tmp_path / "output" / "minimal_function.md").read_text()
    
    # Check that empty sections are not included
    assert "## Purpose" not in content
    assert "## Examples" not in content

def test_write_doc_creates_output_dir(tmp_path, monkeypatch):
    """Test that the output directory is created if it doesn't exist."""
    monkeypatch.chdir(tmp_path)
    
    sections = {"summary": "Test summary"}
    write_doc(sections, "test")
    
    assert (tmp_path / "output").is_dir()
    assert (tmp_path / "output" / "test.md").exists() 