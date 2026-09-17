import string
import getpass
import secrets

COMMON_PASSWORD_FILE = "common_passwords.txt"


def generate_secure_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(
        secrets.choice(characters)
        for _ in range(length)
    )

    return password


def has_predictable_pattern(password):
    lower_password = password.lower()

    predictable_words = [
        "password",
        "admin",
        "welcome",
        "qwerty",
        "letmein",
        "login"
    ]

    for word in predictable_words:
        if word in lower_password:
            return True

    return False


def analyze_password(password):
    # Check whether the password is commonly used
    try:
        with open(COMMON_PASSWORD_FILE, "r") as file:
            common_passwords = {
                line.strip().lower()
                for line in file
                if line.strip()
            }
    except FileNotFoundError:
        common_passwords = set()

    is_common_password = password.lower() in common_passwords

    # Password characteristics
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)

    has_pattern = has_predictable_pattern(password)

    # Calculate strength score
    score = 0

    if len(password) >= 12:
        score += 2

    if len(password) >= 16:
        score += 1

    if has_lowercase:
        score += 1

    if has_uppercase:
        score += 1

    if has_digit:
        score += 1

    if has_special:
        score += 1

    # Determine password strength
    if is_common_password or has_pattern:
        strength = "WEAK"
        score = 0
    elif score <= 2:
        strength = "WEAK"
    elif score <= 4:
        strength = "MEDIUM"
    else:
        strength = "STRONG"

    # Generate security recommendations
    recommendations = []

    if len(password) < 12:
        recommendations.append("Use at least 12 characters.")

    if not has_lowercase:
        recommendations.append("Add lowercase letters.")

    if not has_uppercase:
        recommendations.append("Add uppercase letters.")

    if not has_digit:
        recommendations.append("Add numbers.")

    if not has_special:
        recommendations.append("Add special characters.")

    if is_common_password:
        recommendations.append(
            "This password is commonly used. Choose a completely different password."
        )

    if has_pattern:
        recommendations.append(
            "Avoid predictable words such as password, admin, welcome, or qwerty."
        )

    # Display results
    print("\nPassword Analysis")
    print("-----------------")
    print("Length:", len(password))
    print("Lowercase:", has_lowercase)
    print("Uppercase:", has_uppercase)
    print("Numbers:", has_digit)
    print("Special characters:", has_special)
    print("Common password:", is_common_password)
    print("Predictable pattern:", has_pattern)
    print("Score:", score)
    print("Strength:", strength)

    print("\nRecommendations")
    print("----------------")

    if recommendations:
        for recommendation in recommendations:
            print("- " + recommendation)
    else:
        print("No basic improvements needed.")


# Main program
print("Password Strength Analyzer")
print("==========================")
print("1. Analyze a password")
print("2. Generate a secure password")

choice = input("\nChoose an option (1/2): ")


if choice == "1":

    password = input("Enter your password: ")

    analyze_password(password)


elif choice == "2":

    try:
        length = int(input("Enter password length (minimum 12): "))

        if length < 12:
            print("Password length should be at least 12 characters.")
        else:
            generated_password = generate_secure_password(length)

            print("\nGenerated Secure Password:")
            print(generated_password)

    except ValueError:
        print("Please enter a valid number.")


else:
    print("Invalid option.")