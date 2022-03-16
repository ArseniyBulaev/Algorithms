import controller.routines as cr
import model.types as tp


def main():
    a = tp.Node(1, 2)
    b = tp.Node(1, 4)
    c = tp.Node(1, 0)

    nodes = [a, b, c]

    print(cr.iterative_triangulation(nodes))



if __name__ == "__main__":
    main()