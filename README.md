# Doc Agent

An AI-powered documentation generator that creates technical documentation in Shopify Polaris style from source code.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Smart Documentation Generation**: Automatically generates comprehensive documentation from source code
- **Shopify Polaris Style**: Follows Shopify's design system documentation guidelines
- **Self-Linting**: Includes built-in linting to ensure documentation quality
- **Error Recovery**: Graceful fallback mechanisms when AI processing fails
- **Environment-Based Configuration**: Secure API key management using environment variables

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wringek/doc-agent.git
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

We welcome contributions! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive free software license that allows users to:
- Use the software for any purpose
- Modify the software
- Distribute the software
- Use the software commercially

The only requirement is that the original copyright notice and license terms must be included in any substantial portions of the software.

## Support

For support, please open an issue in the [GitHub repository](https://github.com/wringek/doc-agent/issues).

## Style
See [docs/short_descriptions.md](./docs/short_descriptions.md) for how to craft valid one-line summaries.
