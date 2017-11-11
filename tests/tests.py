import unittest
from tests.validate_collections import ValuesTestCases

def tests():	
	validate_collections_suite = unittest.TestLoader().loadTestsFromTestCase(
		ValuesTestCases)
	return unittest.TestSuite([
		validate_collections_suite,
		])