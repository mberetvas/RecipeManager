# Boilerplate tests for pytest

# import pytest
from src.main import main


def test_placeholder():
    assert True


def test_main_prints_welcome_message(capfd):
    main()
    out, _ = capfd.readouterr()
    assert "Welcome to the Python Template Application!" in out
