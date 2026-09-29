"""
Menu utama CLI.

Loop menu hanya mengatur dispatch ke ``cli.actions``;
error ditangani di level aksi supaya aplikasi tidak
pernah berhenti karena exception.
"""

from .actions import ACTIONS

from .prompts import ask


TITLE = (
    "\n"
    "==============================\n"
    "     STEGANOGRAPHY CLI\n"
    "=============================="
)

MENU = (
    "1. Embed message",
    "2. Extract message",
    "3. Check image capacity",
    "4. Exit",
)

EXIT_CHOICE = "4"


def show_menu():
    """
    Mencetak judul dan daftar menu.
    """

    print(TITLE)

    for item in MENU:

        print(item)


def handle_choice(choice):
    """
    Menjalankan aksi sesuai pilihan user.

    Returns:
        bool: False bila user meminta keluar.
    """

    if choice == EXIT_CHOICE:

        print("Program selesai.")
        return False

    action = ACTIONS.get(choice)

    if action is None:

        print("Pilihan tidak valid.")
        return True

    try:

        action()

    except KeyboardInterrupt:

        print()
        print("Dibatalkan.")

    except Exception as error:

        print(f"Error: {error}")

    return True


def main():
    """
    Menjalankan loop menu sampai user keluar.
    """

    running = True

    while running:

        show_menu()

        running = handle_choice(
            ask("Pilih: ")
        )
