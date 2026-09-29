"""
Helper input untuk CLI.

Semua prompt terkumpul di sini agar ``cli.actions`` fokus
pada logika, bukan pada interaksi terminal.
"""


def ask(prompt, strip=True):
    """
    Mengambil satu baris input dari user.
    """

    value = input(prompt)

    return value.strip() if strip else value


def ask_path(prompt):
    """
    Mengambil path gambar (tanpa spasi di sekitar).
    """

    return ask(prompt)


def heading(title):
    """
    Mencetak judul bergaris.
    """

    print()
    print(title)
    print("-" * len(title))
