from favrip.file_operations import read_csv, write_csv

def test_read_csv_ok_content(tmpdir):
	expected = [["1","google.com"]]

	p = tmpdir.mkdir("sub").join("test.txt")
	p.write("1,google.com")

	actual = read_csv(p.strpath)

	assert actual == expected

def test_read_csv_return_type(tmpdir):
	expected = "1,google.com"
	p = tmpdir.mkdir("sub").join("test.txt")
	p.write("1,google.com")

	actual = read_csv(p.strpath)

	assert isinstance(actual, list)


def test_write_csv(tmpdir):
	p = tmpdir.mkdir("sub").join("test.txt")
	content = [["1", "google.com"]]

	write_csv(content, p.strpath)

	assert p.read() == "1,google.com\n"
