from math import log, exp

def sigmoid(x):
    return 1 / (1 + exp(-x + 2))

def penalty(p):
    return 1 - exp(-p)

def calculate_score(password):
    length = len(password)
    num_specials = sum(1 for c in password if not c.isalnum())
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c.isalnum() for c in password)
    common_patterns = ["123", "password", "qwerty", "admin", "letmein"]

    # component scores
    L = log(length + 1)
    diversity = sum([has_lower, has_upper, has_digit, has_symbol])
    D = sigmoid(diversity)
    C = min(1.0, 0.2* num_specials)
    P = 1.0 if any(p in password.lower() for p in common_patterns) else 0.0

    # weigths
    A, B, Cw, Dw, = 1.2, 2.0, 1.0, 2.0

    raw_score = A * L + B * D + Cw * C - Dw * penalty(P)
    final_score = round(min(5.0, max(1.0, raw_score)), 1)

    return final_score

def suggestions(password, score):
    suggestions = []
    if len(password) < 12:
        suggestions.append("increase password length to at least 12 characters")
    if not any(c.islower() for c in password):
        suggestions.append("Add lowercase letters (a-z)")
    if not any(c.isupper() for c in password):
        suggestions.append("Add uppercase letters (A-Z)")
    if not any(c.isdigit() for c in password):
        suggestions.append("Include numbers (0-9)")
    if not any(not c.isalnum() for c in password):
        suggestions.append("Include special characters (@, #, $, !)")
    if any (p in password.lower() for p in ["123", "password", "qwerty", "admin", "letmein"]):
        suggestions.append("Avoid common patterns like 123")
    
    return suggestions if score < 2.5 else []

if __name__ == "__main__":
    pw = input("Enter a password to evaluate: ")
    score = calculate_score(pw)
    suggestions = suggestions(pw, score)

    print(f"\nPassword Score: {score}/5.0")
    if suggestions:
        print("\nSuggestions: ")
        for s in suggestions:
            print("-", s)
    else:
        print("Your password is strong!")
