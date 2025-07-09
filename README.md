# defi-top10
# DeFi Vulnerabilities Web Application

A web application that displays DeFi vulnerabilities data from a JSON file in a sortable table format with detailed drill-down views.

## Description

This application reads data from the `defi-vulnerabilities-json.json` file and presents it in a web-based table that can be sorted by various criteria. It calculates total losses for each vulnerability and allows users to drill down to see all examples of each vulnerability type.

## Features

- Displays DeFi vulnerabilities in a responsive table with a dark, sinister theme
- Features skull decorations on both sides and a Jolly Roger flag for a serious, threatening appearance
- Dark color scheme with red and orange accents to emphasize the dangerous nature of these vulnerabilities
- Calculates and displays total losses for each vulnerability
- Allows sorting by clicking on column headers:
  - Rank (numeric sorting)
  - Vulnerability name (alphabetical sorting)
  - Occurrence count (numeric sorting)
  - Percentage of losses (percentage of each vulnerability's loss relative to the sum of all 10 vulnerability total losses, sortable with visual indicator)
  - Total losses (numeric sorting)
- Provides detailed drill-down view for each vulnerability showing:
  - All examples of the vulnerability
  - Individual loss amounts for each example
  - Percentage of losses for each example (relative to the vulnerability's total)
  - Total sum of losses
  - Detailed descriptions and references
- Responsive design that works on desktop and mobile devices (skulls hide on smaller screens)

## Installation

1. Make sure you have Python installed (Python 3.6 or higher recommended)
2. **Important**: Install Flask using pip (required for the application to work):

```bash
pip install flask
```

You can verify your setup by running the test script:

```bash
python test_app.py
```

## Usage

1. Make sure the `defi-vulnerabilities-json.json` file is in the same directory as the application
2. Run the application:

```bash
python app.py
```

3. Open your web browser and navigate to `http://127.0.0.1:5000/`
4. The main table will be displayed with the vulnerability data including total losses
5. Click on any column header to sort the table by that column (all sortable columns have visual indicators)
   - The "Percentage of Losses" column shows each vulnerability's total loss as a percentage of the sum of all 10 vulnerability total losses and can be sorted by clicking the column header
   - The "Total Losses" column shows the absolute value of losses for each vulnerability
6. Click on any vulnerability name to view its detailed page showing:
   - All examples of that vulnerability
   - Individual loss amounts
   - Percentage of each example's loss relative to the total
   - Total sum of losses
   - Detailed descriptions and references
7. Use the "Back to All Vulnerabilities" link to return to the main table

## Project Structure

- `app.py`: The Flask application that serves the web pages and calculates total losses
- `templates/index.html`: The HTML template with the main table and sorting functionality
- `templates/detail.html`: The HTML template for the detailed drill-down view of each vulnerability
- `defi-vulnerabilities-json.json`: The source data file containing DeFi vulnerabilities information
- `test_app.py`: A test script to verify the application setup
