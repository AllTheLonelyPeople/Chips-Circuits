######################################################################
# tupletest.py
# Tom Kamstra
# Minor programmeren
######################################################################


def main():
    gates = [(1,2), (2,3)]
    netlist = [(1,2)]
    AllWires = [(1,2), (2,2), (2,3)]


    solution = {
        (1,2) : [(1,2), (2,2), (2,3)]
    }

    print(solution)
if __name__ == "__main__":
    main()