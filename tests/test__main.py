from cachetronaut import main


def test__main__happy_path():
    assert main.main() == 0
