import unittest
from triangulation import Triangle
from triangulation import Node


class TestTriangle(unittest.TestCase):

  def setUp(self):
    nodes = [Node(1, 1), Node(2, 2), Node(3, 3)]
    triangles = []
    self.triangle = Triangle(nodes, triangles, number=1)


  def test_get_other_nodes(self):
    actual = self.triangle.nodes[1:]
    expected = self.triangle.get_other_nodes(self.triangle.nodes[0])

    actual.sort(key=lambda node: node.x)
    expected.sort(key=lambda node: node.x)

    self.assertEqual(expected, actual)



if __name__ == "__main__":
  unittest.main()