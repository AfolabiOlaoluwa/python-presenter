import pytest

from python_presenter.core.presenters.base_presenter import BasePresenter


class SampleObject:
    def __init__(self, name):
        self.name = name


class SamplePresenter(BasePresenter):
    def custom_method(self):
        return f"Processed {self.obj.name}"


@pytest.fixture
def sample_object():
    """
    Fixture to create a sample object for testing.

    Returns:
        SampleObject: A test object with a name attribute.
    """
    return SampleObject("Test Object")


@pytest.fixture
def sample_view_context():
    """
    Fixture to create a sample view context.

    Returns:
        dict: A dictionary representing a view context.
    """
    return {"context_key": "value"}


@pytest.fixture
def base_presenter(sample_object, sample_view_context):
    """
    Fixture to create a BasePresenter instance.

    Args:
        sample_object: A sample object fixture.
        sample_view_context: A sample view context fixture.

    Returns:
        BasePresenter: A BasePresenter instance for testing.
    """
    return BasePresenter(sample_object, sample_view_context)


class TestBasePresenterInitialization:
    def test_initialization_with_view_context(self, base_presenter):
        """
        Test BasePresenter initialization with object and view context.
        """
        assert base_presenter.obj.name == "Test Object"
        assert base_presenter.view_context == {"context_key": "value"}

    def test_initialization_with_none(self):
        """
        Verify behavior when 'obj' is None.
        """
        presenter = BasePresenter(None)

        assert presenter.obj is None
        assert presenter.view_context is None

    @pytest.mark.parametrize("expected_context", [
        {"key": "value"},  # Standard dictionary
        None,              # None value
        123,               # Integer
        "string",          # String
        [],                # Empty list
        set(),             # Empty set
        object()           # Object instance
    ])
    def test_view_context_variations(self, sample_object, expected_context):
        """
        Comprehensive test for view context variations.
        
        Args:
            sample_object: Fixture providing a sample object
            expected_context: Parametrized view context to test
        """
        presenter = BasePresenter(sample_object, expected_context)

        assert presenter.view_context == expected_context

    @pytest.mark.parametrize("context_modifier", [
        lambda ctx: {"new_key": "new_value"},  # Dictionary modification
        lambda ctx: None,                      # Set to None
        lambda ctx: 456                        # Change to another type
    ])
    def test_view_context_mutation(self, base_presenter, context_modifier):
        """
        Test multiple ways of mutating view context.

        Args:
            base_presenter: Fixture providing a base presenter
            context_modifier: Function to modify view context
        """
        modified_context = context_modifier(base_presenter.view_context)
        base_presenter.view_context = modified_context

        assert base_presenter.view_context == modified_context


class TestBasePresenterAttributeAccess:
    def test_attribute_access(self, base_presenter):
        """
        Test object attributes are accessible through the presenter.
        """
        assert base_presenter.obj.name == "Test Object"

    def test_obj_mutability(self, sample_object):
        """
        Verify 'obj' can be reassigned after initialization.
        """
        presenter = BasePresenter(sample_object)
        new_object = SampleObject("New Object")

        presenter.obj = new_object

        assert presenter.obj == new_object
        assert presenter.obj.name == "New Object"


class TestBasePresenterMethodLookup:
    def test_custom_method_in_subclass(self, sample_object):
        """
        Test custom method in a BasePresenter subclass.
        """
        presenter = SamplePresenter(sample_object)

        assert presenter.custom_method() == "Processed Test Object"

    def test_custom_method_with_incomplete_object(self):
        """
        Test custom method behavior with incomplete object.
        """
        class IncompleteObject:
            pass

        incomplete_obj = IncompleteObject()
        presenter = SamplePresenter(incomplete_obj)

        with pytest.raises(AttributeError):
            presenter.custom_method()

    def test_subclass_overrides_getattr(self, sample_object):
        """
        Test behavior when a subclass overrides __getattr__.
        """
        class OverridingPresenter(BasePresenter):
            def __getattr__(self, attr):
                return f"Overridden {attr}"

        presenter = OverridingPresenter(sample_object)

        assert presenter.some_attribute == "Overridden some_attribute"


class TestBasePresenterErrorHandling:
    def test_getattr_missing_attribute(self, base_presenter):
        """
        Ensure __getattr__ raises AttributeError for nonexistent attributes.
        """
        with pytest.raises(AttributeError, match="object has no attribute 'nonexistent_attribute'"):
            base_presenter.nonexistent_attribute

    def test_getattr_not_handled(self):
        """
        Test when __getattr__ is called for an unexpected attribute.
        """
        presenter = BasePresenter(object())

        with pytest.raises(AttributeError):
            presenter.non_existent


def test_package_import():
    """
    Verify the package can be imported.
    """
    import python_presenter
    assert python_presenter is not None