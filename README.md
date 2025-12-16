Autonomous Insurance Claims Processing Agent 
Overview

This project implements a lightweight autonomous agent to process FNOL (First Notice of Loss) documents.
The agent extracts key claim-related fields from FNOL text, validates the presence of mandatory information, and routes the claim to the appropriate workflow based on predefined business rules.

The focus of this solution is clarity, explainability, and simplicity rather than complex machine learning models.

Features

Rule-based extraction of structured data from FNOL text documents

Validation of mandatory fields with clear identification of missing information

Claim classification and workflow routing using business rules

Basic fraud detection using keyword matching in the incident description

Structured JSON output for system integration

Human-readable decision summary for claim reviewers

Uses only Python standard libraries (no external dependencies)

Claim Routing Logic
Condition	Route	Priority
Missing mandatory fields	Manual Review	1 (Highest)
Fraud indicators detected	Investigation Flag	2
Injury-related claim	Specialist Queue	3
Estimated damage < ₹25,000	Fast-track	4
Estimated damage ≥ ₹25,000	Standard Review	5 (Default)
Fraud Keywords Checked

The agent scans the claim description for the following keywords:

fraud

staged

inconsistent

suspicious

fabricated

false claim

If any of these are detected, the claim is flagged for investigation.

Fields Extracted
Policy Information

Policy Number

Policyholder Name

Effective Dates

Incident Information

Incident Date

Incident Time

Location

Description

Involved Parties

Claimant

Contact Details

Asset Details

Asset Type

Asset ID

Estimated Damage

Claim Information

Claim Type

Attachments

Initial Estimate

Tech Stack

Language: Python 3.8+

Dependencies: None (pure Python)

Pattern Matching: Regular Expressions (re module)

Output Format: JSON

Project Structure
autonomous-fnol-claims-agent/
│
├── fnol_agent.py        # Main FNOL processing agent
├── README.md            # Project documentation
├── sample_fnol.txt      # Sample FNOL input document
├── requirements.txt     # Python version requirement
└── test_cases.py        # Optional test cases

Installation
Prerequisites

Python 3.8 or higher

Setup

No external libraries are required.

git clone <repository-url>
cd autonomous-fnol-claims-agent

How to Run
python fnol_agent.py


The agent will:

Parse the FNOL document

Extract relevant fields

Validate mandatory information

Apply routing rules

Output structured JSON and a readable summary

Design Notes

This solution intentionally uses rule-based logic to keep the decision-making transparent and easy to audit.
Such an approach is commonly used in early-stage claim triage systems, where explainability and reliability are more important than model complexity.
