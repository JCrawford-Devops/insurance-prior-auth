def evaluate_prior_auth_rule(insurance_provider: str, procedure_code: str) -> dict:
    payer = insurance_provider.strip().lower()
    code = procedure_code.strip().upper()

    rules = {
        ("blue cross", "D2740"): {
            "prior_auth_required": True,
            "rule_reason": "Crowns typically require prior authorization for this payer."
        },
        ("blue cross", "D1110"): {
            "prior_auth_required": False,
            "rule_reason": "Routine adult prophylaxis typically does not require prior authorization."
        },
        ("delta dental", "D4341"): {
            "prior_auth_required": True,
            "rule_reason": "Periodontal scaling and root planing often requires prior authorization."
        },
        ("delta dental", "D2740"): {
            "prior_auth_required": True,
            "rule_reason": "Crowns are commonly reviewed for prior authorization."
        },
        ("aetna", "D2950"): {
            "prior_auth_required": True,
            "rule_reason": "Core buildup may require documentation and prior authorization review."
        },
    }

    match = rules.get((payer, code))
    if match:
        return match

    return {
        "prior_auth_required": False,
        "rule_reason": "No specific prior authorization rule matched for this payer and procedure code."
    }