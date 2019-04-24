glob_var = 99

def main():
	global glob_var
	print(glob_var)
	glob_var = 100
	print(glob_var)


if __name__ == "__main__":
	main()