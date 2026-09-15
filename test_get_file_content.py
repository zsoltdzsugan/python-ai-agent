from functions.get_file_content import get_file_content

# Test large file
result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")


# Test main.py
result = get_file_content("calculator", "main.py")
print("Result for 'main.py':")
print(result)


# Test pkg/calculator.py
result = get_file_content("calculator", "pkg/calculator.py")
print("Result for 'pkg/calculator.py':")
print(result)


# Test file outside working directory
result = get_file_content("calculator", "/bin/cat")
print("Result for '/bin/cat':")
print(result)


# Test nonexistent file
result = get_file_content("calculator", "pkg/does_not_exist.py")
print("Result for 'pkg/does_not_exist.py':")
print(result)
