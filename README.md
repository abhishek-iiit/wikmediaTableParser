# Wikipedia FIFA World Cup Finals Extractor

This project extracts FIFA World Cup finals data from Wikipedia and appends it to a Google Sheet using the Google Sheets API.

## Features
- Configurable Wikipedia source and table selector
- Extracts Year, Winner, Score, Runners-up for first N finals
- Appends data to Google Sheets via API
- All settings via `.env` file

## Setup
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file (see `.env` example in repo).
3. Run the main script:
   ```bash
   python -m wikipedia_parser.main
   ```

## Docker Usage
Build and run the container:
```bash
docker build -t wikipedia-parser .
docker run --env-file .env wikipedia-parser
```

## Project Structure
- `wikipedia_parser/` — Source code package
- `tests/` — Unit tests (to be added)
- `.env` — Environment variables
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation

## Configuration
All configuration is in `.env` (see `toDo.md` for details).

## License
MIT
