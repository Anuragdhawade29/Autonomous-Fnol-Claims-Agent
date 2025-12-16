import json
import re
from typing import Dict, List, Tuple

class FNOLAgent:
    """
    Autonomous Insurance Claims Processing Agent
    Processes First Notice of Loss (FNOL) documents and routes claims
    """

    # Mandatory fields required for processing
    MANDATORY_FIELDS = {
        'policy_number': 'Policy Information',
        'policyholder_name': 'Policy Information',
        'incident_date': 'Incident Information',
        'incident_time': 'Incident Information',
        'location': 'Incident Information',
        'description': 'Incident Information',
        'claimant': 'Involved Parties',
        'asset_type': 'Asset Details',
        'estimated_damage': 'Asset Details',
        'claim_type': 'Claim Type'
    }

    FAST_TRACK_THRESHOLD = 25000  # ₹25,000
    FRAUD_KEYWORDS = ['fraud', 'staged', 'inconsistent', 'suspicious', 'fabricated', 'false claim']

    def __init__(self):
        self.extracted_fields = {}
        self.missing_fields = []
        self.fraud_flags = []

    def extract_field(self, text: str, pattern: str) -> str:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else None

    def parse_fnol(self, fnol_text: str) -> Dict:
        patterns = {
            'policy_number': r'(?:Policy Number|POL)[:\s]+([A-Z0-9]+)',
            'policyholder_name': r'(?:Policyholder Name|Insured)[:\s]+([A-Za-z\s]+)',
            'incident_date': r'(?:Incident Date|Date of Loss)[:\s]+([0-9\-/]+)',
            'incident_time': r'(?:Incident Time|Time of Loss)[:\s]+([0-9:]+\s*(?:AM|PM)?)',
            'location': r'(?:Location|Address of Loss)[:\s]+([^\n]+)',
            'description': r'(?:Description|Accident Description)[:\s]+([^\n]+)',
            'claimant': r'(?:Claimant|Insured)[:\s]+([A-Za-z\s]+)',
            'contact_details': r'(?:Contact|Phone)[:\s]+([0-9\-\+\s]+)',
            'asset_type': r'(?:Asset Type|Vehicle Type)[:\s]+([A-Za-z\s]+)',
            'asset_id': r'(?:Asset ID|VIN|Registration)[:\s]+([A-Z0-9]+)',
            'estimated_damage': r'(?:Estimated Damage|Estimate Amount)[:\s]+(?:₹|Rs\.?)?([0-9]+)',
            'claim_type': r'(?:Claim Type)[:\s]+([A-Za-z\s]+)',
            'attachments': r'(?:Attachments?)[:\s]+([^\n]+)',
            'initial_estimate': r'(?:Initial Estimate)[:\s]+(?:₹|Rs\.?)?([0-9]+)'
        }

        for field, pattern in patterns.items():
            value = self.extract_field(fnol_text, pattern)
            if value:
                self.extracted_fields[field] = value

        for field, category in self.MANDATORY_FIELDS.items():
            if field not in self.extracted_fields:
                self.missing_fields.append({
                    "field": field,
                    "category": category
                })

        description = self.extracted_fields.get("description", "").lower()
        for keyword in self.FRAUD_KEYWORDS:
            if keyword in description:
                self.fraud_flags.append(keyword)

        return self.extracted_fields

    def classify_and_route(self) -> Tuple[str, str]:
        reasoning = []

        if self.missing_fields:
            fields = ", ".join(f["field"] for f in self.missing_fields)
            return "Manual Review", f"Missing mandatory fields: {fields}"

        if self.fraud_flags:
            return "Investigation Flag", f"Suspicious keywords detected: {', '.join(self.fraud_flags)}"

        claim_type = self.extracted_fields.get("claim_type", "").lower()
        if "injury" in claim_type:
            return "Specialist Queue", "Injury-related claim requires specialist handling"

        try:
            damage = float(self.extracted_fields.get("estimated_damage", 0))
            if damage < self.FAST_TRACK_THRESHOLD:
                return (
                    "Fast-track",
                    f"Estimated damage ₹{damage:,.2f} is below fast-track threshold"
                )
            else:
                return (
                    "Standard Review",
                    f"Estimated damage ₹{damage:,.2f} exceeds fast-track threshold"
                )
        except:
            return "Manual Review", "Invalid or missing damage estimate"

    def process_claim(self, fnol_text: str) -> Dict:
        self.parse_fnol(fnol_text)
        route, reasoning = self.classify_and_route()

        return {
            "extractedFields": self.extracted_fields,
            "missingFields": [f["field"] for f in self.missing_fields],
            "recommendedRoute": route,
            "reasoning": reasoning,
            "fraudFlags": self.fraud_flags if self.fraud_flags else None
        }


def print_summary(result: Dict):
    print("\nSUMMARY")
    print("-" * 80)

    claim_type = result["extractedFields"].get("claim_type", "unknown") \
        .lower().replace(" ", "_")

    route = result["recommendedRoute"].upper().replace("-", "_")

    print(f"Claim Type: {claim_type}")
    print(f"Recommended Route: {route}")
    print(f"Risk Flags: {', '.join(result['fraudFlags']) if result['fraudFlags'] else 'None'}")
    print(f"Missing Fields: {', '.join(result['missingFields']) if result['missingFields'] else 'None'}")

    print("\nDecision Reasoning:")
    print(result["reasoning"])


def main():
    sample_fnol = """
    Policy Number: POL123456
    Policyholder Name: John Doe
    Incident Date: 15-03-2024
    Incident Time: 18:30 PM
    Location: Mumbai, Maharashtra
    Description: Rear-end collision at traffic signal.
    Claimant: John Doe
    Contact Details: 9876543210
    Asset Type: Car
    Asset ID: MH12AB1234
    Estimated Damage: 8500
    Claim Type: Vehicle Damage
    Attachments: Photos, FIR
    Initial Estimate: 8500
    """

    agent = FNOLAgent()
    result = agent.process_claim(sample_fnol)

    # JSON Output (System Friendly)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Human Readable Summary
    print_summary(result)


if __name__ == "__main__":
    main()
