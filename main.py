from carbonpy.namer import Namer
from carbonpy.error import ValencyError

if __name__ == "__main__":
    print("Type `/help` to get usage information.")

    while True:
        try:
            compound_struct = input("Condensed structure > ").strip()
            if compound_struct == "/help":
                print(__doc__)
            else:
                compound = Namer(compound_struct)
                print(f"\n{compound}\n{compound.molecular_formula()}\n{compound.analyser()}\n")

        except EOFError:  # Ctrl-D on Windows
            print("\nExiting...")
            raise SystemExit

        except ValencyError as e:
            print(e)
