#!/usr/bin/env bash
set -e

# 1. Create the directory structure
mkdir -p doc-agent/src/doc_agent
mkdir -p doc-agent/docs/adr
mkdir -p doc-agent/docs/notes
mkdir -p doc-agent/tests
mkdir -p doc-agent/output
mkdir -p doc-agent/examples

# 2. Create empty code files
touch doc-agent/src/doc_agent/{__init__.py,__main__.py,agent.py,agent_loop.py}
touch doc-agent/src/doc_agent/{draft.py,ingestion.py,lint.py,outline.py,pipeline.py,publish.py,tools.py}

# 3. Create evaluators and linters directories
mkdir -p doc-agent/src/doc_agent/evaluators
mkdir -p doc-agent/src/doc_agent/linters
touch doc-agent/src/doc_agent/evaluators/{__init__.py,ai_eval.py,heuristics.py,rubric.py,types.py}
touch doc-agent/src/doc_agent/linters/{__init__.py,short_description.py}

# 4. Create test files
touch doc-agent/tests/{__init__.py,test_agent.py,test_agent_loop.py,test_agent_loop_main.py}
touch doc-agent/tests/{test_agent_loop_mock.py,test_cli.py,test_evaluators.py,test_heuristics.py}
touch doc-agent/tests/{test_ingestion.py,test_lint.py,test_outline.py,test_publish.py}

# 5. Create supporting files
touch doc-agent/{requirements.txt,README.md,CONTRIBUTING.md,LICENSE,pyproject.toml,pytest.ini}

# 6. Create .gitignore with the desired entries
cat > doc-agent/.gitignore << 'EOF'
.venv/
__pycache__/
*.pyc
output/
docs/**/_build/
.coverage
.DS_Store
EOF

echo "Scaffold complete! Navigate into doc-agent/ and start coding."
