from fastnanoid import generate


def generate_oid(length: int = 21):
    """Generates unique value with NanoID of given length."""
    return generate(size=length)
