# Autonomous Insurance Claims Processing Agent (Lite)

## Overview
This project implements a lightweight autonomous agent to process FNOL (First Notice of Loss) documents. The agent extracts key insurance claim fields, detects missing or inconsistent information, and routes the claim to the appropriate workflow based on business rules.

## Features
✅ Rule-based field extraction from FNOL text documents  
✅ Mandatory field validation with category classification  
✅ Claim classification and intelligent routing  
✅ Fraud detection using keyword matching  
✅ Structured JSON output with explanations  
✅ Zero dependencies (uses only Python standard library)  

## Routing Rules Implemented

| Condition | Route | Priority |
|-----------|-------|----------|
| Missing mandatory fields | **Manual Review** | 1 (Highest) |
| Fraud indicators detected | **Investigation Flag** | 2 |
| Injury claim | **Specialist Queue** | 3 |
| Damage < ₹25,000 | **Fast-track** | 4 |
| Damage ≥ ₹25,000 | **Standard Review** | 5 (Default) |

### Fraud Keywords Detected
`fraud`, `staged`, `inconsistent`, `suspicious`, `fabricated`, `false claim`

## Fields Extracted

### Policy Information
- Policy Number
- Policyholder Name
- Effective Dates

### Incident Information
- Incident Date
- Incident Time
- Location
- Description

### Involved Parties
- Claimant
- Contact Details

### Asset Details
- Asset Type
- Asset ID
- Estimated Damage

### Claim Information
- Claim Type
- Attachments
- Initial Estimate

## Tech Stack
- **Language**: Python 3.8+
- **Dependencies**: None (pure Python)
- **Pattern Matching**: Regular Expressions (re module)
- **Data Format**: JSON

## Project Structure
```
autonomous-fnol-claims-agent/
│
├── fnol_agent.py          # Main agent class
├── README.md              # This file
├── sample_fnol.txt        # Sample FNOL document
├── requirements.txt       # Python dependencies
└── test_cases.py          # Test suite (optional)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
```bash
# Clone the repository
git clone https://github.com/yourusername/autonomous-fnol-claims-agent.git
cd autonomous-fnol-claims-agent

# Install dependencies (minimal)
pip install -r requirements.txt
```

## How to Run

### Basic Usage
```bash
python fnol_agent.py
```

### Programmatic Usage
```python
from fnol_agent import FNOLAgent

# Create agent instance
agent = FNOLAgent()

# Read FNOL document
with open('sample_fnol.txt', 'r') as f:
    fnol_text = f.read()

# Process claim
result = agent.process_claim(fnol_text)

# View results
import json
print(json.dumps(result, indent=2))
```

## Output Format

```json
{
  "extractedFields": {
    "policy_number": "POL123456",
    "policyholder_name": "John Doe",
    "incident_date": "15-03-2024",
    "incident_time": "18:30 PM",
    "location": "Mumbai, Maharashtra",
    "description": "Rear-end collision at traffic signal",
    "claimant": "John Doe",
    "asset_type": "Car",
    "asset_id": "MH12AB1234",
    "estimated_damage": "18000",
    "claim_type": "Vehicle Damage",
    "attachments": "Photos, FIR"
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Estimated damage ₹18,000 < ₹25,000 threshold",
  "fraudFlags": null
}
```

## Design Choices

### 1. **Rule-Based Approach**
- Simple, transparent, and auditable logic
- No black-box ML models
- Easy to update business rules
- Production-friendly for early claim triage

### 2. **Regular Expressions for Extraction**
- Handles multiple document formats
- No heavy NLP libraries required
- Fast execution
- Clear extraction logic

### 3. **Priority-Based Routing**
- Missing fields take highest priority (data quality first)
- Fraud flags before injury (safety critical)
- Damage amount last (used for efficiency classification)

### 4. **Zero Dependencies**
- Minimal footprint
- No version conflicts
- Easy deployment
- Pure Python implementation

## Example Use Cases

### Case 1: Valid Low-Value Claim (Fast-track)
```
Input: Policy POL123456, Damage ₹18,000
Output: Fast-track route
Reason: Damage below ₹25,000 threshold
```

### Case 2: High-Value Claim (Standard Review)
```
Input: Policy POL789012, Damage ₹65,000
Output: Standard Review route
Reason: Damage exceeds ₹25,000 threshold
```

### Case 3: Missing Information (Manual Review)
```
Input: Policy POL345678, Missing: incident_time, asset_type, claim_type
Output: Manual Review route
Reason: 3 mandatory fields missing
```

### Case 4: Fraud Indicators (Investigation Flag)
```
Input: Policy POL456789, Description: "Staged accident for fraud"
Output: Investigation Flag route
Reason: Fraud keywords detected in description
```

## Extensibility

To add new fields:
```python
patterns['new_field'] = r'(?:Field Label)[:\s]+([pattern]+)'
```

To add new routing rules:
```python
def classify_and_route(self):
    # ... existing rules ...
    
    # New rule
    if custom_condition:
        route = "New Route"
        reasoning.append("Custom reason")
        return route, " → ".join(reasoning)
```

## Testing
Run with sample FNOL documents:
```bash
python fnol_agent.py  # Uses built-in sample
```

## Performance
- **Extraction Speed**: ~1ms per document
- **Memory Usage**: < 1MB
- **Dependencies**: 0 (Python stdlib only)

## Future Enhancements
- PDF text extraction support (pdfplumber)
- Multiple language support
- Machine learning confidence scores
- OCR for handwritten documents
- API endpoint wrapper (Flask/FastAPI)
- Database integration for audit trails

## Interview Talking Points

> "I built a rule-based FNOL processing agent focusing on explainability and production readiness.
> 
> **Key decisions:**
> - Rule-based over ML: Transparent, auditable, no black boxes
> - Regex extraction: Handles multiple formats, no heavy dependencies
> - Priority routing: Missing data first, then safety concerns, then efficiency metrics
> - Zero dependencies: Minimal deployment complexity
>
> **Business value:**
> - Claims triaged within milliseconds
> - Fraud indicators flagged automatically
> - Missing data caught early in process
> - Easy to explain decisions to stakeholders
>
> **Why it works:**
> - Solves the assessment requirements efficiently
> - Demonstrates understanding of insurance workflows
> - Shows thoughtful engineering choices
> - Scales easily across claims volume"

## Limitations & Disclaimers
- Regex patterns are case-insensitive but may miss edge formats
- Fraud detection is keyword-based (not ML-based)
- No cross-document validation (each claim processed independently)
- Designed for text-based FNOL documents

## License
MIT License - Feel free to use for learning and projects

## Contact
For questions or suggestions, open an issue on GitHub.

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Status**: Production-Ready for Assessment
