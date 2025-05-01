# Doc Agent

A Python-based tool that combines heuristics and AI-powered evaluations to improve text quality, with a focus on error messages and user-facing content.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

### Core Functionality
- **AI-Powered Text Generation**: Generates context-aware text based on scenarios and style guidelines
- **Static Heuristics**: Checks for forbidden words, passive voice, and other common issues
- **AI-Based Linting**: Iteratively improves text quality through AI-powered suggestions
- **Maximum Iteration Control**: Prevents infinite loops with configurable iteration limits

### AI Evaluations
- **Clarity & Actionability**: Rates text clarity (1-5) and checks if it's immediately actionable
- **Tone & Brand Voice**: Evaluates alignment with specified brand voice (1-5)
- **Empathy**: Assesses emotional intelligence and provides improvement suggestions
- **Additional Evaluations**:
  - Inclusivity & Bias Screening
  - Readability for Non-Native Speakers
  - Cognitive Load & Conciseness
  - Accessibility Compliance
  - Message Consistency
  - User Trust & Confidence
  - Internationalization Readiness

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/doc-agent.git
   cd doc-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

## Usage

### Quick Start

The simplest way to use Doc Agent is through the command line:

```bash
python src/doc_agent/agent_loop.py
```

This will:
1. Generate an error message for a sample scenario
2. Apply heuristic and lint fixes
3. Run AI evaluations for clarity, tone, and empathy
4. Display the results and final text

Example output:
```
--- AI Evaluations ---
Clarity (5/5): The message clearly states what is required.
Actionable? True. The user knows exactly what to do.

Tone (4/5, aligned=True):
  The tone is friendly and empathetic.

Empathy (4/5):
  Shows understanding and provides clear guidance.

--- Final Text ---
"Enter your email to continue."
```

### Programmatic Usage

```python
from doc_agent.agent_loop import run_agent_loop
from doc_agent.evaluators.ai_eval import (
    evaluate_clarity_and_actionability,
    evaluate_tone,
    evaluate_empathy
)

# Generate and improve text
text = run_agent_loop(
    scenario="User submits a form without filling a required field",
    style="Shopify inline error",
    forbidden_file="src/doc_agent/evaluators/forbidden_words.txt",
    max_iters=5
)

# Run evaluations
clarity = evaluate_clarity_and_actionability(text)
tone = evaluate_tone(text, brand_voice="friendly and empathetic")
empathy = evaluate_empathy(text)

# Access results
print(f"Clarity: {clarity['clarity_score']}/5")
print(f"Actionable? {clarity['actionable']}")
print(f"Tone: {tone['tone_score']}/5")
print(f"Empathetic? {empathy['empathetic']}")
```

## Testing

The project includes comprehensive test coverage for all major components:

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=doc_agent --cov-report=term-missing

# Run specific test files
pytest tests/test_agent_loop.py
pytest tests/test_lint.py
```

### Test Structure
- `test_agent_loop.py`: Tests for the main agent loop functionality
- `test_lint.py`: Tests for linting and self-improvement features
- `test_agent_loop_main.py`: Tests for AI evaluations and error handling

## Project Structure

```
doc-agent/
├── src/
│   └── doc_agent/
│       ├── agent_loop.py      # Main agent loop implementation
│       ├── evaluators/
│       │   ├── ai_eval.py     # AI-powered evaluations
│       │   └── heuristics.py  # Static heuristic checks
│       ├── draft.py           # Text generation tools
│       └── lint.py            # Linting functionality
├── tests/
│   ├── test_agent_loop.py
│   ├── test_lint.py
│   └── test_agent_loop_main.py
└── requirements.txt
```

## Development

### Adding New Evaluators

1. Add your evaluator function in `src/doc_agent/evaluators/ai_eval.py`
2. Use the `@handle_openai_call` decorator for error handling
3. Return a dictionary with appropriate evaluation metrics
4. Add tests in `tests/test_agent_loop_main.py`

### Error Handling

The project includes robust error handling for:
- OpenAI API errors
- JSON parsing errors
- Maximum iteration limits
- Invalid inputs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

The MIT License is a permissive free software license that allows users to:
- Use the software for any purpose
- Modify the software
- Distribute the software
- Use the software commercially

The only requirement is that the original copyright notice and license terms must be included in any substantial portions of the software.

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Style
See [docs/short_descriptions.md](./docs/short_descriptions.md) for how to craft valid one-line summaries.
