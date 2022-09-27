import unittest

print("Running unit tests from api/test directory...")

loader = unittest.TestLoader()
start_dir = 'test'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)

print("Running tests is complete")