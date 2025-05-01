# Doc-Agent: AI-Powered Documentation Assistant

Doc-Agent is an intelligent documentation generation and improvement system that combines Large Language Models (LLMs) with static analysis to create high-quality technical documentation.

## Features

- 🤖 AI-powered documentation generation with smart retry logic
- 📝 Comprehensive evaluation system (heuristics, AI, rubrics)
- 🔄 Iterative improvement with progress tracking
- 📊 Multiple quality metrics (clarity, tone, empathy)
- 🎯 Customizable documentation styles and formats
- 🚀 Development optimization modes for rapid iteration

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/doc-agent.git
cd doc-agent
```

2. Set up your environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: `.venv\Scripts\activate`
pip install -r requirements.txt
```

3. Configure your environment:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

4. Run the documentation agent:
```bash
# Generate documentation
python -m doc_agent generate --scenario "Write a function that sorts a list" --style "Clear and concise"

# Process an existing document
python -m doc_agent process path/to/source.py
```

## Command-Line Interface

Doc-Agent provides two main commands: `generate` and `process`.

### Generate Command

Generate and evaluate documentation from scratch:

```bash
python -m doc_agent generate [options]
```

#### Options

- `--scenario TEXT` (Required): The scenario to generate text for
- `--style TEXT`: The writing style to use (default: "Clear and professional")
- `--max-iters N`: Maximum improvement iterations (default: 5)
- `--eval LIST`: Comma-separated list of evaluators to run
- `--forbidden-file PATH`: Custom forbidden words file
- `--show-details`: Show detailed evaluation reports
- `--json`: Output results in JSON format
- `-v, --verbose`: Increase output verbosity
- `-q, --quiet`: Suppress all output except errors and final result

Development options:
- `--no-eval`: Skip all evaluations (fastest, for development)
- `--fast`: Use only fast evaluators (no AI calls)

### Process Command

Process an existing document through the improvement pipeline:

```bash
python -m doc_agent process [options] SOURCE_PATH
```

#### Options

- `SOURCE_PATH` (Required): Path to the source file to process
- `--forbidden-file PATH`: Custom forbidden words file
- `--json`: Output results in JSON format
- `-v, --verbose`: Increase output verbosity
- `-q, --quiet`: Suppress all output except errors and final result

## Evaluators

Doc-Agent includes several evaluators that can be combined to assess documentation quality. Use the `--eval` flag to specify which evaluators to run.

### Fast Evaluators (No AI)

1. **heuristics**
   - Forbidden word detection
   - Readability scoring
   - Pattern matching
   - Style compliance checks
   - Fast, deterministic evaluation

2. **rubric**
   - Documentation structure validation
   - Quality criteria checking
   - Format verification
   - Standard compliance
   - Quick structural analysis

### AI-Powered Evaluators

1. **clarity**
   - Assesses text clarity (1-5 scale)
   - Checks actionability
   - Provides clarity improvement suggestions
   - Uses AI for semantic understanding

2. **empathy**
   - Evaluates emotional intelligence (1-5 scale)
   - Checks user-friendliness
   - Suggests empathy improvements
   - Considers reader perspective

3. **tone**
   - Analyzes writing tone
   - Checks brand voice alignment
   - Scores tone appropriateness (1-5)
   - Suggests tone improvements

### Usage Examples

1. Fast evaluation (no AI calls):
```bash
python -m doc_agent generate \
  --scenario "Document the API endpoint" \
  --eval "heuristics,rubric" \
  --fast
```

2. Comprehensive evaluation:
```bash
python -m doc_agent generate \
  --scenario "Write error message" \
  --eval "heuristics,rubric,clarity,empathy,tone" \
  --show-details
```

3. Focus on user experience:
```bash
python -m doc_agent generate \
  --scenario "Write installation guide" \
  --eval "clarity,empathy" \
  --style "User-friendly"
```

4. Quick development iteration:
```bash
python -m doc_agent generate \
  --scenario "Draft API docs" \
  --no-eval
```

## Project Structure

```
doc-agent/
├── src/doc_agent/          # Core package
│   ├── __main__.py        # Entry point & CLI
│   ├── agent.py           # Agent implementation
│   ├── pipeline.py        # Pipeline orchestration
│   ├── agent_loop.py      # Processing loop
│   ├── draft.py           # Content generation
│   ├── tools.py           # Utility functions
│   ├── lint.py           # Linting functionality
│   ├── outline.py        # Document structure
│   ├── publish.py        # Output generation
│   ├── ingestion.py      # Input processing
│   ├── evaluators/       # Quality assessment
│   └── linters/         # Style checking
├── docs/                 # Documentation
│   ├── architecture.md   # System design
│   └── adr/             # Architecture decisions
├── tests/               # Test suite
└── examples/            # Usage examples
```

## Architecture

The system follows a pipeline architecture with these key components:

1. **Input Processing** (`ingestion.py`): Parse requirements and style preferences
2. **Content Generation** (`draft.py`): Generate initial documentation using LLMs
3. **Quality Assessment** (`evaluators/`): Evaluate content using multiple metrics
4. **Pipeline Processing** (`pipeline.py`): Coordinate the documentation flow
5. **Agent Management** (`agent.py`): Handle AI interactions and improvements
6. **Publication** (`publish.py`): Format and output final documentation

For detailed architecture information, see [docs/architecture.md](docs/architecture.md).

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for their powerful language models
- The Python community for excellent documentation tools
- All contributors to this project
