# flatten.sh
#!/usr/bin/env bash
set -e

# Script to flatten the nested "doc-agent/doc-agent" layer
# Run from the outer project directory

# List of items to move from inner to root
items=("src" "tests" "docs" "tools.py" "setup.sh" "pytest.ini" "README.md" ".gitignore")
inner="doc-agent"

for item in "${items[@]}"; do
  if [ -e "$inner/$item" ]; then
    mv "$inner/$item" .
    echo "Moved $inner/$item to ./"
  fi
done

# Remove the now-empty inner directory
rmdir "$inner" && echo "Removed $inner directory"

echo "Flattening complete."
