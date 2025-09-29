def is_eligiblae_for_loan(income : float, age: int, employement_status: str) -> bool:
    return (income >= 50000) and (age>=21) and (employement_status == 'employed')
