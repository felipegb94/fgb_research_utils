## Standard Library Imports
import time

## Library Imports

## Local Imports

class Timer:
	def __init__(self, name=None):
		self.name = name
		self._start = None
		self.elapsed = 0.0

	def start(self):
		if self._start is not None:
			raise RuntimeError('Timer already started...')
		self._start = time.perf_counter()

	def stop(self):
		if self._start is None:
			raise RuntimeError('Timer not yet started...')
		end = time.perf_counter()
		self.elapsed += end - self._start
		self._start = None

	def __enter__(self):  # Setup
		self.start()
		# return self so that we can use it outside of the with block, e.g. "with Timer as t:"
		return self 

	def __exit__(self, *args):  # Teardown
		self.stop()
		if self.name: print('[{}] - Elapsed: {} seconds.'.format(self.name, self.elapsed))
		else: print('Elapsed: {}'.format(self.elapsed))
				

