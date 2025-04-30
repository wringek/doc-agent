#!/usr/bin/env bash
set -e

# 1. Create the directory structure
mkdir -p doc-agent/.cursor
mkdir -p doc-agent/src/agent
mkdir -p doc-agent/templates
mkdir -p doc-agent/tests
mkdir -p doc-agent/docs

# 2. Create empty code files
touch doc-agent/src/{__init__.py,main.py,tools.py}
touch doc-agent/src/agent/{ingestion.py,outline.py,draft.py,lint.py,publish.py}

# 3. Create test stubs
touch doc-agent/tests/{test_ingestion.py,test_outline.py,test_lint.py}

# 4. Create supporting files
touch doc-agent/{requirements.txt,README.md}

# 5. Create .gitignore with the desired entries
cat > doc-agent/.gitignore << 'EOF'
.venv/
__pycache__/
*.pyc
docs/
EOF

echo "Scaffold complete! Navigate into doc-agent/ and start coding."
