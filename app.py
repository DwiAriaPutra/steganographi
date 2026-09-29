"""
Entry point CLI steganografi.

Jalankan::

    python app.py

Seluruh logika ada di paket ``cli``; file ini hanya
menjalankan main loop.
"""

from cli.menu import main


if __name__ == "__main__":

    try:

        main()

    except (KeyboardInterrupt, EOFError):

        print()
        print("Program selesai.")
