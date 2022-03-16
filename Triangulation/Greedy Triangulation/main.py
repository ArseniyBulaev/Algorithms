import helper.types as htypes
import helper.routines as hrout
import triangulation.methods as traingmeth



def main():
	n = int(input("n = "))  # Number of points
	nodes = hrout.generate_nodes(n)
	triangulation = traingmeth.greedy_triangulation(nodes)
	hrout.plot_segments(triangulation)



if __name__ == "__main__":
	main()