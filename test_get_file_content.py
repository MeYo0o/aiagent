from functions.get_file_content import get_file_content


def test():
    # Test truncation with lorem.txt (22,000+ chars, should truncate at 10,000)
    print('get_file_content("calculator", "lorem.txt"):')
    print()
    result = get_file_content("calculator", "lorem.txt")
    print(f"Content length: {len(result)} characters")
    print(f"Truncated: {'truncated' in result}")
    print(f"End of content: ...{result[-80:]}")
    print()

    # Test reading main.py
    print('get_file_content("calculator", "main.py"):')
    print()
    print(get_file_content("calculator", "main.py"))
    print()

    # Test reading pkg/calculator.py
    print('get_file_content("calculator", "pkg/calculator.py"):')
    print()
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    # Test path outside working directory
    print('get_file_content("calculator", "/bin/cat"):')
    print()
    print(get_file_content("calculator", "/bin/cat"))
    print()

    # Test non-existent file
    print('get_file_content("calculator", "pkg/does_not_exist.py"):')
    print()
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    test()
