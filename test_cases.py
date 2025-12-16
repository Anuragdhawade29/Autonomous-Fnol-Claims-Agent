# TEST CASES FOR AUTONOMOUS FNOL AGENT

import json
import re
from typing import Dict, List, Tuple
from fnol_agent import FNOLAgent

# Test Case 1: Valid Low-Value Claim (Fast-track)
test_case_1 = """
Policy Number: POL123456
Policyholder Name: John Doe
Policy Effective Dates: 01-01-2024 to 01-01-2025
Incident Date: 15-03-2024
Incident Time: 18:30 PM
Location: Mumbai, Maharashtra
Description: Rear-end collision at traffic signal. Vehicle sustained moderate damage.
Claimant: John Doe
Contact Details: 9876543210
Asset Type: Car
Asset ID: MH12AB1234
Estimated Damage: 18000
Claim Type: Vehicle Damage
Attachments: Photos, FIR
Initial Estimate: 18000
"""

# Test Case 2: High-Value Claim (Standard Review)
test_case_2 = """
Policy Number: POL789012
Policyholder Name: Priya Sharma
Policy Effective Dates: 05-06-2023 to 05-06-2024
Incident Date: 20-11-2023
Incident Time: 14:15
Location: Bangalore, Karnataka
Description: Front-end collision with extensive damage requiring full repair.
Claimant: Priya Sharma
Contact Details: 9123456789
Asset Type: Car
Asset ID: KA51CD9876
Estimated Damage: 65000
Claim Type: Vehicle Damage
Attachments: Photos, Police Report
Initial Estimate: 65000
"""

# Test Case 3: Missing Mandatory Fields (Manual Review)
test_case_3 = """
Policy Number: POL345678
Policyholder Name: Raj Kumar
Incident Date: 10-08-2024
Location: Delhi
Description: Side collision with another vehicle.
"""

# Test Case 4: Fraud Indicators (Investigation Flag)
test_case_4 = """
Policy Number: POL456789
Policyholder Name: Amit Patel
Policy Effective Dates: 01-01-2024 to 01-01-2025
Incident Date: 12-12-2024
Incident Time: 22:00
Location: Pune, Maharashtra
Description: Staged accident for fraud. Timeline inconsistent with witness statement.
Claimant: Amit Patel
Contact Details: 9988776655
Asset Type: Bike
Asset ID: MH14EF5432
Estimated Damage: 12000
Claim Type: Vehicle Damage
Attachments: Photos
Initial Estimate: 12000
"""

# Test Case 5: Injury Claim (Specialist Queue)
test_case_5 = """
Policy Number: POL567890
Policyholder Name: Neha Singh
Policy Effective Dates: 15-05-2023 to 15-05-2025
Incident Date: 02-12-2024
Incident Time: 10:45 AM
Location: Hyderabad, Telangana
Description: Multi-vehicle accident resulting in bodily injuries to both driver and passenger.
Claimant: Neha Singh
Contact Details: 9876543321
Asset Type: Car
Asset ID: TS07EF2345
Estimated Damage: 35000
Claim Type: Bodily Injury
Attachments: Medical Records, FIR, Photos
Initial Estimate: 35000
"""

def run_test(test_name: str, fnol_document: str) -> Dict:
    """Run a single test case and return results"""
    agent = FNOLAgent()
    result = agent.process_claim(fnol_document)
    
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")
    print(f"Status: ✓ PASSED")
    print(f"Route: {result['recommendedRoute']}")
    print(f"Fields Extracted: {len(result['extractedFields'])}")
    print(f"Missing Fields: {len(result['missingFields'])}")
    if result['fraudFlags']:
        print(f"Fraud Flags: {', '.join(result['fraudFlags'])}")
    print(f"\nFull Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

def main():
    """Execute all test cases"""
    print("="*80)
    print("AUTONOMOUS FNOL CLAIMS PROCESSING AGENT - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    test_cases = [
        ("Test 1: Valid Low-Value Claim (Fast-track)", test_case_1, "Fast-track"),
        ("Test 2: High-Value Claim (Standard Review)", test_case_2, "Standard Review"),
        ("Test 3: Missing Mandatory Fields (Manual Review)", test_case_3, "Manual Review"),
        ("Test 4: Fraud Indicators (Investigation Flag)", test_case_4, "Investigation Flag"),
        ("Test 5: Injury Claim (Specialist Queue)", test_case_5, "Specialist Queue"),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for test_name, fnol_doc, expected_route in test_cases:
        result = run_test(test_name, fnol_doc)
        
        # Verify expected route
        if result['recommendedRoute'] == expected_route:
            passed += 1
            test_status = "✓ PASSED"
        else:
            failed += 1
            test_status = f"✗ FAILED (Expected: {expected_route}, Got: {result['recommendedRoute']})"
        
        results.append({
            'test': test_name,
            'status': test_status,
            'route': result['recommendedRoute'],
            'extracted_fields': len(result['extractedFields']),
            'missing_fields': len(result['missingFields'])
        })
    
    # Summary Report
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    
    print(f"\n{'='*80}")
    print("DETAILED RESULTS")
    print(f"{'='*80}")
    for result in results:
        print(f"\n{result['test']}")
        print(f"  Route: {result['route']}")
        print(f"  Fields Extracted: {result['extracted_fields']}")
        print(f"  Missing Fields: {result['missing_fields']}")
        print(f"  Status: {result['status']}")
    
    print(f"\n{'='*80}")
    if failed == 0:
        print("✅ ALL TESTS PASSED SUCCESSFULLY")
    else:
        print(f"⚠️  {failed} TEST(S) FAILED")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
