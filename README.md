# Doc Agent

An AI-powered documentation generator that creates technical documentation in Shopify Polaris style from source code.

## Features

- **Smart Documentation Generation**: Automatically generates comprehensive documentation from source code
- **Shopify Polaris Style**: Follows Shopify's design system documentation guidelines
- **Self-Linting**: Includes built-in linting to ensure documentation quality
- **Error Recovery**: Graceful fallback mechanisms when AI processing fails
- **Environment-Based Configuration**: Secure API key management using environment variables

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
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

4. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the documentation generator on a source file:

```bash
python src/main.py path/to/your/source/file
```

The generated documentation will be saved in the `docs/` directory.

## Project Structure

```
doc-agent/
├── src/
│   ├── agent/
│   │   ├── ingestion.py  # Source code parsing and metadata extraction
│   │   ├── outline.py    # Documentation structure generation
│   │   ├── draft.py      # Content generation using OpenAI
│   │   ├── lint.py       # Documentation quality checks
│   │   └── publish.py    # Documentation file generation
│   └── main.py          # Main entry point
├── docs/                # Generated documentation
├── examples/            # Example source files
└── tests/              # Test suite
```

## Dependencies

- Python 3.11+
- OpenAI API client
- python-dotenv
- httpx
- pytest (for testing)

## Error Handling

The system includes robust error handling:
- Automatic retries with exponential backoff for API calls
- Fallback to basic documentation when AI processing fails
- Timeout management for API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Support

For support, please [add your support contact information]

## Style
See [docs/short_descriptions.md](./docs/short_descriptions.md) for how to craft valid one-line summaries.
