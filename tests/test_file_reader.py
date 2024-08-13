import pytest

from escapewright import FileReader


def test_file_reader():
    fr = FileReader()
    assert fr is not None
    assert fr.file_name is None

    fr.load_file("./tests/fr_dict_test.txt")
    assert fr.file_name == "./tests/fr_dict_test.txt"

    dictionary = fr.to_dict()

    assert dictionary is not None

    assert dictionary["string"] == "string"
    assert dictionary["int"] == 1
    assert dictionary["float"] == 1.0
    assert dictionary["bool"] is True

    assert isinstance(dictionary["string"], str)
    assert isinstance(dictionary["int"], int)
    assert isinstance(dictionary["float"], float)
    assert isinstance(dictionary["bool"], bool)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
