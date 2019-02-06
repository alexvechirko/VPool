import pickle
import numpy


def read_file(filename):
	"""
	Function to read pickle file and give its data

	Args:
		filename: Name of pickle file

	Returns:
		Data dictionary that was stored in .pkl format.
	"""
	file = filename
	data = {}
	with (open(file, "rb")) as openfile:
		data = pickle.load(openfile)
	return data


def unpickle_data(pickle_file_name):
	"""
	Utility function to read data if it is present in a pickle
	file and write content into the corresponding files.

	Args:
		pickle_file_name: Pickle file to be read

	Returns:
		Adjacency matrix and distance matrix.
	"""
	data_dictionary = read_file(pickle_file_name)
	numpy_adjacency_matrix = data_dictionary['admissibility_matrix']
	distance_matrix = data_dictionary['distance_matrix']

	adjacency_matrix = []
	if (type(numpy_adjacency_matrix).__name__ != 'list'):
		adjacency_matrix = numpy_adjacency_matrix.values.tolist()
	else:
		adjacency_matrix = numpy_adjacency_matrix
	return adjacency_matrix, distance_matrix


def pickle_data(adjacency_matrix, distance_matrix, pickle_file_name):
	"""
	Utility function to take data and pickle the dictionary into 
	the given file.

	Args:
		adjacency_matrix: Adjacency matrix to be pickled
		distance_matrix: Distance matrix to be pickled
		pickle_file_name: Name of file which stores data
	"""
	pickle_dictionary = {}
	pickle_dictionary['admissibility_matrix'] = adjacency_matrix
	pickle_dictionary['distance_matrix'] = distance_matrix

	pickle_file = open(pickle_file_name,'wb')
	pickle.dump(pickle_dictionary, pickle_file)
	pickle_file.close()


if __name__ == '__main__':
	pass