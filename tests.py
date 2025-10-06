from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test():

	#result = get_file_content("calculator", "main.py")
	#print(f"Result for current directory: \n {result}")

	#result = get_file_content("calculator", "pkg/calculator.py")
	#print(f"\nResult for 'pkg' directory: \n {result}")

	#result = get_file_content("calculator", "/bin/cat")
	#print(f"\nResult for '/bin' directory: \n {result}")

	#result = get_file_content("calculator", "pkg/does_not_exist.py")
	#print(f"\nResult for '../' directory: \n {result}")

	#result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
	#print(f"\nResult for lorem.txt: \n {result}")

	#result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
	#print(f"\nResult for pkg/morelorem.txt: \n {result}")

	#result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
	#print(f"\nResult for /tmp/temp.txt: \n {result}")

	result = run_python_file("calculator", "main.py")
	print(f"Result for : {result}")
	
	result = run_python_file("calculator", "main.py", ["3 + 5"])
	print(f"Result for : {result}")
	
	result = run_python_file("calculator", "tests.py")
	print(f"Result for : {result}")
	
	result = run_python_file("calculator", "../main.py")
	print(f"Result for : {result}")
	
	result = run_python_file("calculator", "nonexistent.py")
	print(f"Result for : {result}")


if __name__ == "__main__":
    test()
