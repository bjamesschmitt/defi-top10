import json
import os
import re
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def parse_loss_amount(loss_str):
    """Parse loss amount from string to float value in millions."""
    if not loss_str or loss_str == "Undisclosed":
        return 0

    # Remove dollar sign, commas, and any text in parentheses
    clean_str = loss_str.replace('$', '').replace(',', '')
    clean_str = re.sub(r'\s*\(.*\)', '', clean_str)

    # Extract the numeric part
    match = re.search(r'([\d.]+)', clean_str)
    if not match:
        return 0

    amount = float(match.group(1))

    # Convert to millions if necessary
    if "million" in clean_str.lower():
        return amount
    if "billion" in clean_str.lower():
        return amount * 1000

    # If the amount is already in full dollars (not in millions)
    if amount > 1000000:
        return amount / 1000000

    return amount

def calculate_total_losses(examples):
    """Calculate total losses from examples."""
    total = 0
    for example in examples:
        # Check for loss_millions field first (new format)
        if 'loss_millions' in example:
            total += float(example.get('loss_millions', 0))
        else:
            # Fall back to parsing loss string (old format)
            total += parse_loss_amount(example.get('loss', '0'))
    return total

@app.route('/')
def index():
    # Read the JSON file
    with open('defi-vulnerabilities-json.json', 'r') as file:
        data = json.load(file)

    # Extract vulnerabilities data
    vulnerabilities = data.get('vulnerabilities', [])

    # Calculate total losses for each vulnerability
    for vuln in vulnerabilities:
        # Use total_loss_millions from JSON if available
        if 'total_loss_millions' in vuln:
            total_loss = float(vuln.get('total_loss_millions', 0))
        else:
            # Otherwise calculate from examples
            examples = vuln.get('examples', [])
            total_loss = calculate_total_losses(examples)

        vuln['total_loss'] = total_loss
        vuln['total_loss_formatted'] = f"${total_loss:.2f} million"

    # Calculate the sum of all vulnerability total losses
    total_losses_sum = sum(vuln['total_loss'] for vuln in vulnerabilities) if vulnerabilities else 0

    # Calculate percentage of losses relative to the sum of all vulnerability total losses
    for vuln in vulnerabilities:
        if total_losses_sum > 0:
            percentage = (vuln['total_loss'] / total_losses_sum) * 100
            vuln['percentage_of_total'] = percentage
            vuln['percentage_of_total_formatted'] = f"{percentage:.1f}%"
        else:
            vuln['percentage_of_total'] = 0
            vuln['percentage_of_total_formatted'] = "0.0%"

    return render_template('index.html', 
                          title=data.get('title', ''),
                          total_losses=data.get('total_losses', ''),
                          vulnerabilities=vulnerabilities)

@app.route('/vulnerability/<int:rank>')
def vulnerability_detail(rank):
    # Read the JSON file
    with open('defi-vulnerabilities-json.json', 'r') as file:
        data = json.load(file)

    # Find the vulnerability with the given rank
    vulnerability = None
    for vuln in data.get('vulnerabilities', []):
        if vuln.get('rank') == rank:
            vulnerability = vuln
            break

    if not vulnerability:
        return redirect(url_for('index'))

    # Calculate total losses
    # Use total_loss_millions from JSON if available
    if 'total_loss_millions' in vulnerability:
        total_loss = float(vulnerability.get('total_loss_millions', 0))
    else:
        # Otherwise calculate from examples
        examples = vulnerability.get('examples', [])
        total_loss = calculate_total_losses(examples)

    vulnerability['total_loss'] = total_loss
    vulnerability['total_loss_formatted'] = f"${total_loss:.2f} million"

    # Calculate percentage of losses for each example
    examples = vulnerability.get('examples', [])
    for example in examples:
        # Get the loss amount for this example
        if 'loss_millions' in example:
            example_loss = float(example.get('loss_millions', 0))
        else:
            example_loss = parse_loss_amount(example.get('loss', '0'))

        # Calculate percentage (avoid division by zero)
        if total_loss > 0:
            percentage = (example_loss / total_loss) * 100
            example['percentage'] = percentage
            example['percentage_formatted'] = f"{percentage:.1f}%"
        else:
            example['percentage'] = 0
            example['percentage_formatted'] = "0.0%"

    return render_template('detail.html',
                          title=data.get('title', ''),
                          vulnerability=vulnerability)

# Ensure templates directory exists
os.makedirs('templates', exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
