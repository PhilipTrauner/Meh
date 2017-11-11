import unittest
from meh import validate_value


class ValuesTestCases(unittest.TestCase):
	"""Tests for validate_value and make_value"""
	
	def test_can_recursive_lists_be_validated(self):
		"""
		Validate if unsupported data types inside lists in lists detection
		works.
		""" 
		invalid_list = [[lambda x: True, "a", "b", "c", (lambda x: False)], 
				1, 2, lambda x: False]
		valid_list = [1, [1, 2, ("test", )], ["foo"]]
		self.assertFalse(validate_value(invalid_list))
		self.assertTrue(validate_value(valid_list))

	def test_can_lists_be_validated(self):
		"""
		Validate if unsupported data types inside list detection works.
		"""
		invalid_list = [lambda x: False, "a", 1, 2]
		valid_list = [1, 2]
		self.assertFalse(validate_value(invalid_list))
		self.assertTrue(validate_value(valid_list))


	def test_can_recursive_tuples_be_validated(self):
		"""
		Validate if unsupported data types inside lists in lists detection
		works.
		""" 
		invalid_tuple = ((lambda x: True, "a", "b", "c", (lambda x: False)), 
				1, 2, lambda x: False)
		valid_tuple = (1, (1, 2, ("test", )), ("foo"))
		self.assertFalse(validate_value(invalid_tuple))
		self.assertTrue(validate_value(valid_tuple))

	def test_can_tuples_be_validated(self):
		"""
		Validate if unsupported data types inside tuple detection works.
		"""
		invalid_tuple = (lambda x: False, "a", 1, 2)
		valid_tuple = (b"test", 1, 2, 3)
		self.assertFalse(validate_value(invalid_tuple))
		self.assertTrue(validate_value(valid_tuple))

	def test_can_recursive_dicts_be_validated(self):
		"""
		Validate if unsupported data types inside recursive dict key and value 
		combination detection works.
		"""
		invalid_dict = {1 : {"test" : lambda x: True}, 2 : lambda x: True}
		valid_dict = {1 : "foo", 2 : {"baz" : "lol"}}
		self.assertFalse(validate_value(invalid_dict))
		self.assertTrue(validate_value(valid_dict))


	def test_can_dicts_be_validated(self):
		"""
		Validate if unsupported data types inside dict key and value 
		combination detection works.
		"""
		invalid_dict = {1 : "test", 2 : lambda x : True}
		valid_dict = {1 : "foo", 2 : 3}
		self.assertFalse(validate_value(invalid_dict))
		self.assertTrue(validate_value(valid_dict))	


if __name__ == "__main__":
	unittest.main()
