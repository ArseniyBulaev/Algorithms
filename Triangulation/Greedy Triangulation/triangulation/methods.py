import helper.routines as hrout


def greedy_triangulation(nodes):
	def intersect(s1, s2):
		def signed_area(a, b, c):
			return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

		def intersect_1d(a, b, c, d):
			if a > b : a, b = b, a
			if c > d : c, d = d, c
			return max(a, c) <= min(b, d)

		a = s1.start_point
		b = s1.end_point
		c = s2.start_point
		d = s2.end_point	

		return intersect_1d(a.x, b.x, c.x, d.x) and\
			   intersect_1d(a.y, b.y, c.y, d.y) and\
		       signed_area(a, b, c) * signed_area(a, b, d) <= 0 and\
		       signed_area(c, d, a) * signed_area(c, d, b) <= 0

	segments = hrout.generate_segments(nodes)
	segments.sort(key=lambda x: x.length())
	
	triangulation = []


	while segments:
		new_segment = segments.pop(0)

		for segment in triangulation:

			if (new_segment.start_point != segment.start_point and new_segment.end_point != segment.end_point) and\
			   (new_segment.end_point != segment.start_point and new_segment.start_point != segment.end_point):

				if intersect(new_segment, segment):
					break
		else:
			triangulation.append(new_segment)

	return triangulation
