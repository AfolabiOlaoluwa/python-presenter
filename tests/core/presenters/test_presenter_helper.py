import sys
from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from python_presenter.core.presenters.presenter_helper import present


@dataclass
class User:
    name: str
    email: str
    role: str = "user"
    active: bool = True


class UserPresenter:
    def __init__(self, obj, context=None):
        self.obj = obj
        self.context = context

    def display_caps_name(self):
        return self.obj.name.upper()

    def display_caps_email(self):
        return self.obj.email.upper()


@pytest.fixture
def user() -> User:
    return User(name="John Doe", email="john@example.com")


@pytest.fixture
def mock_presenter_module():
    """
    Fixture to mock the `presenters.presenter` module and set up the inspect.getmodule mock.
    """
    mock_module_path = "presenters.presenter"
    sys.modules[mock_module_path] = sys.modules[__name__]

    mock_module = Mock()
    mock_module.__name__ = "tests.core.presenters.test_presenter_helper"

    with patch('inspect.getmodule', return_value=mock_module):
        yield


class TestPresenterBasicFunctionality:
    """Tests basic presenter functionality"""

    def test_present_with_explicit_presenter(self, user: User):
        """Test present() when presenter_class is explicitly provided"""
        result = present(user, UserPresenter, context=None)

        assert isinstance(result, UserPresenter)
        assert result.obj == user
        assert result.display_caps_name() == "JOHN DOE"

    def test_present_with_invalid_presenter(self, user: User):
        """Test present() with invalid presenter class (missing obj parameter)"""

        class InvalidPresenter:
            def __init__(self):
                pass

        with pytest.raises(TypeError):
            present(user, InvalidPresenter, context=None)


class TestPresenterAutoDiscovery:
    """Tests automatic presenter discovery functionality"""

    def test_present_method_discoverability_without_custom_presenter_class(self, user: User, mock_presenter_module):
        """
        A test for the present() function to ensure it works correctly with automatic presenter discovery.

        This test dynamically simulates the module structure required by the `present` function
        to resolve the presenter class. It verifies the expected behavior of `present` without
        requiring external files.

        Inherited Fixture Feature:
        - The `UserPresenter` class is dynamically injected into `sys.modules` under the
          `presenters.presenter` module path, simulating an external module.
        - The `inspect.getmodule` call is mocked to return the correct module path
          (`tests.core.presenters.test_presenter_helper`) for accurate resolution of the
          `current_module`.
        - `sys.modules[mock_module_path] = sys.Modules[__name__]` dynamically maps the
          test file's module (`__name__`) to the expected `presenters.presenter` module path.

        Asserts:
            - The returned object is an instance of `UserPresenter`.
            - The presenter instance encapsulates the original `User` object.
        """
        presenter = present(user, context=None)

        assert isinstance(presenter, UserPresenter)
        assert presenter.obj == user

    def test_present_with_custom_presenter(self, user: User):
        """Test present() method when a custom presenter is explicitly provided."""
        presenter = present(user, presenter_class=UserPresenter, context=None)

        assert isinstance(presenter, UserPresenter)
        assert presenter.obj == user


class TestPresenterErrorHandling:
    """Tests error handling scenarios"""

    def test_missing_presenter_class(self):
        """Test behavior when presenter class doesn't exist in module"""

        mock_module = Mock(__name__='python_presenter.core.models')

        with patch('python_presenter.core.presenters.presenter_helper.getmodule', return_value=mock_module):
            with patch('python_presenter.core.presenters.presenter_helper.import_module') as mock_import:
                mock_import.return_value = Mock(spec=[])

                with pytest.raises(AttributeError):
                    present(User("Test", "test@example.com"), context=None)

    def test_invalid_presenter_class(self, user: User):
        """Test behavior when invalid presenter class is provided"""

        class InvalidPresenter:
            def __init__(self):
                pass  # No obj parameter

        with pytest.raises(TypeError):
            present(user, InvalidPresenter, context=None)
