# Python built-in imports
import os
import sys
import warnings
from argparse import ArgumentParser, Namespace

# Relative imports
import favrip

def parse_args() -> Namespace:
	""" Wrapper to establish an ArgumentParser and return script CLI args
		and kwargs.
	
		:return Namespace: CLI arguments in object form
	"""
	parser = ArgumentParser()
	parser.add_argument(
		"input_csv",
		help="CSV of ranked domains"
	)
	parser.add_argument(
		"--parallelism",
		type=int,
		default=100,
		help="Maximum number of simultaneous HTTP requests"
	)
	parser.add_argument(
		"--output_directory",
		default=os.getcwd(),
		help="Directory where results files will be written"
	)

	parser.add_argument(
		"--timeout",
		type=int,
		default=5
	)

	return parser.parse_args()

def main() -> int:
	"""	CLI entrypoint to the Favrip script for ripping favicons from domains.

		:return status_code: Status code - 0 for success
	"""
	args = parse_args()
	status_code = 1
	try:
		print("Running favrip with arguments...\n{}".format(
			"\n".join(
				[f"{key}: {value}" for key, value in vars(args).items()])))

		status_code = favrip.run(
			args.input_csv,
			args.parallelism,
			args.timeout,
			args.output_directory
		)
	except Exception as e:
		print(f"\nFailed due to: {e.__class__.__name__}: {str(e)}")
	return status_code

sys.exit(main())