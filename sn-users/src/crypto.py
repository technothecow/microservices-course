import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password for secure storage.

    Args:
        password: The password to hash

    Returns:
        The hashed password as a string
    """
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Return the hashed password as a string
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        password: The password to check
        hashed_password: The stored hash to check against

    Returns:
        True if password matches, False otherwise
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
