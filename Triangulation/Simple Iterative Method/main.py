import controller.routines as cr
import model.types as tp


def main():
    a = tp.Edge(1, 2)
    b = tp.Edge(1, 4)
    c = tp.Edge(1, 0)

    edges = [a, b, c]

    print(cr.iterative_triangulation(edges))



if __name__ == "__main__":
    main()