import sys
from dataclasses import dataclass
from unittest.mock import patch

import pytest
from django import template
from django.template import Context
from django.template.engine import Engine

from python_presenter.core.templatetags.presenter_tag import present_object

register = template.Library()


@dataclass
class Project:
    price_detail: str
    project_name: str
    property_address: str
    property_unit_type: str


class ProjectPresenter:
    def __init__(self, obj, context=None):
        self.obj = obj
        self.context = context

    def price_detail(self):
        return self.obj.price_detail

    def project_name(self):
        return self.obj.project_name

    def property_address(self):
        return self.obj.property_address

    def property_unit_type(self):
        return self.obj.property_unit_type.upper()

    @property
    def labels(self):
        return {
            'price_detail': 'Price Detail',
            'project_name': 'Project Name',
            'property_address': 'Property Address',
            'property_unit_type': 'Property Unit Type',
        }


@pytest.fixture
def project():
    return Project(
        price_detail="500,000 USD",
        project_name="Skylark Towers",
        property_address="123 Elm Street",
        property_unit_type="apartment",
    )


@pytest.fixture
def template_context(project):
    return Context({'project': project})


@pytest.fixture
def mock_present_function():
    with patch("python_presenter.core.templatetags.presenter_tag.present",
               return_value=ProjectPresenter) as mock_present:
        yield mock_present


class TestPresenterTag:
    def test_present_object_with_presenter_class(self, project, mock_present_function, template_context):
        """Test present_object function with a specific presenter class"""
        present_object(template_context, project, ProjectPresenter)

        mock_present_function.assert_called_once_with(project, ProjectPresenter, context=template_context)

    def test_present_object_without_presenter_class(self, project, mock_present_function, template_context):
        """Test present_object function without specifying a presenter class"""
        present_object(template_context, project)

        mock_present_function.assert_called_once_with(project, None, context=template_context)

    @pytest.mark.django_db
    def test_django_template_tag_registration(self, project, mock_present_function, template_context):
        """Test that the template tag is properly registered in Django"""
        @register.simple_tag(takes_context=True)
        def present_object(context, obj, presenter_class=None):
            """A mock implementation of present_object for testing."""
            presenter_class = mock_present_function.return_value
            presenter_instance = presenter_class(obj, context=context)
            return presenter_instance

        engine = Engine.get_default()
        engine.template_libraries['presenter_tag'] = register
        template_tag_library = engine.template_libraries['presenter_tag']

        template_content = """
            {% load presenter_tag %}
            {% present_object project as presented_project %}
            <li><strong>{{ presented_project.labels.project_name }}:</strong> {{ presented_project.project_name }}</li>
            <li><strong>{{ presented_project.labels.property_unit_type }}:</strong> {{ presented_project.property_unit_type }}</li>
        """

        templ = engine.from_string(template_content)
        rendered_output = templ.render(template_context)

        expected_output = """
            <li><strong>Project Name:</strong> Skylark Towers</li>
            <li><strong>Property Unit Type:</strong> APARTMENT</li>
        """

        assert 'presenter_tag' in engine.template_libraries
        assert hasattr(template_tag_library, 'tags')
        assert 'present_object' in template_tag_library.tags
        assert rendered_output.strip() == expected_output.strip()

    @patch('python_presenter.core.templatetags.presenter_tag.template', None)
    def test_django_import_error_handling(self):
        """Test graceful handling when Django template module is not available"""
        with patch.dict(sys.modules, {'django': None}):
            import importlib
            import python_presenter.core.templatetags.presenter_tag
            importlib.reload(python_presenter.core.templatetags.presenter_tag)

            assert hasattr(python_presenter.core.templatetags.presenter_tag, 'present_object')

    def test_present_object_integration(self, project, template_context):
        """Test actual integration with the presenter system"""
        presented = present_object(template_context, project, ProjectPresenter)

        assert hasattr(presented, 'price_detail')
        assert hasattr(presented, 'project_name')
        assert hasattr(presented, 'property_address')
        assert hasattr(presented, 'property_unit_type')
        assert hasattr(presented, 'labels')

        assert presented.price_detail() == "500,000 USD"
        assert presented.project_name() == "Skylark Towers"
        assert presented.property_address() == "123 Elm Street"
        assert presented.property_unit_type() == "APARTMENT"

    @pytest.mark.parametrize("attribute,expected_label", [
        ('price_detail', 'Price Detail'),
        ('project_name', 'Project Name'),
        ('property_address', 'Property Address'),
        ('property_unit_type', 'Property Unit Type')
    ])
    def test_presenter_labels(self, project, template_context, attribute, expected_label):
        """Test that all expected labels are present and correctly formatted"""
        presented = present_object(template_context, project, ProjectPresenter)

        assert attribute in presented.labels
        assert isinstance(presented.labels[attribute], str)
        assert presented.labels[attribute] != ""
        assert presented.labels[attribute] == expected_label

    @patch('python_presenter.core.templatetags.presenter_tag.present')
    def test_present_object_error_handling(self, mock_present_function, project, template_context):
        """Test error handling in present_object function"""
        mock_present_function.side_effect = Exception("Presentation error")

        with pytest.raises(Exception) as exc_info:
            present_object(template_context, project, ProjectPresenter)

        assert str(exc_info.value) == "Presentation error"
