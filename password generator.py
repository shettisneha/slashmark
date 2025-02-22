import random
import string

def generate_password(length=12):
    """Generate a strong, secure password."""
    if length < 8:
        print("Password length should be at least 8 characters for better security.")
        return None

    # Define the character sets
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Ensure the password includes at least one character from each set
    all_characters = lower + upper + digits + symbols
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Fill the rest of the password length with random choices from all characters
    password += random.choices(all_characters, k=length - 4)

    # Shuffle the password to avoid predictable patterns
    random.shuffle(password)

    return ''.join(password)

# Main program
if __name__ == "__main__":
    print("Welcome to the Password Generator!")
    try:
        length = int(input("Enter the desired password length (minimum 8): "))
        password = generate_password(length)
        if password:
            print(f"Your generated password is: {password}")
    except ValueError:
        print("Please enter a valid number.")
