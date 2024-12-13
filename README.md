# Python Presenter

## Overview

The Python Presenter is a library designed to address common architectural challenges in web application development by introducing a flexible, testable layer between application logic and presentation. Inspired by architectural patterns that separate concerns, this library provides a robust solution for managing view-specific logic and data preparation.

## The Problem

As web applications grow in complexity, developers often encounter several architectural challenges:

1. **Logic Complexity**: Application logic becomes increasingly complex, handling multiple responsibilities.
2. **Presentation Logic Creep**: Template files begin to contain formatting, computation, and business logic.
3. **Testing Difficulties**: Complex logic becomes challenging to test in isolation.

## The Presenter Solution

The Python Presenter library introduces a dedicated layer that:

- Encapsulates presentation-specific data preparation
- Separates concerns between data retrieval and presentation
- Provides a clean, testable interface for presentation logic
- Simplifies application logic responsibilities

## Key Benefits

- **Improved Testability**: Logic can be unit tested without setting up complex application environments
- **Separation of Concerns**: Cleanly separates data aggregation from presentation
- **Flexible Architecture**: Easily extensible to handle complex presentation requirements
- **Enhanced Maintainability**: Reduces complexity in application logic and templates

## Installation

```bash
pip install python-presenter
```

## Basic Usage

### Simple Example

In your module, define a `presenter.py` file, and map the model datapoints you want extensively. 

```python
# presenter.py
from python_presenter import BasePresenter as base_presenter

class ProjectPresenter(base_presenter):
    def price_detail(self):
        return self.obj.price_detail

    def project_name(self):
        return self.obj.project_name

    def property_address(self):
        return self.obj.property_address

    def property_unit_type(self):
        result = self.obj.property_unit_type
        return property_types[result].value if result in property_types.__members__ else result

    @property
    def labels(self):
        return {
            'price_detail': 'Price Detail',
            'project_name': 'Project Name',
            'property_address': 'Property 7 Address', # you can author labels to be different from database column labels on the fly.
            'property_unit_type': 'Property Unit Type',
        }
```
This defines the specific object you want to render on the HTML template. Any data from the database that is not explicitly defined here will not appear on the template when using `{% present_object model_name_or_app_name %}` in the template file. This approach allows you to preprocess and customize the data before presenting it in the template, keeping the logic out of the template itself. Additionally, it provides an opportunity to test the object at the code level, ensuring better maintainability and separation of concerns.

#### Django Templating:

The `presenter_tag` is provided as a template tag to render objects using a specified presenter class. To use it, include the tag in your template with `{% load presenter_tag %}`. Then, use the predefined `present_object` method to render the objects defined in the presenter file you created. See below:

```html    
<!-- templates/whatever_template_file.html -->

{% extends "base.html" %}
{% load static %}

{% load presenter_tag %}

{% block content %}
    {% for project in projects %}
        {% present_object project as presented_project %}
            <li><strong>{{ presented_project.labels.price_detail }}:</strong> {{ presented_project.price_detail }}</li>
            <li><strong>{{ presented_project.labels.project_name }}:</strong> {{ presented_project.project_name }}</li>
            <li><strong>{{ presented_project.labels.expected_profit }}:</strong> {{ presented_project.expected_profit }}</li>
            <li><strong>{{ presented_project.labels.property_address }}:</strong> {{ presented_project.property_address }}</li>
            <li><strong>{{ presented_project.labels.property_unit_type }}:</strong> {{ presented_project.property_unit_type }}</li>
            <br><br>
            <!-- Other project details -->
    {% endfor %}
{% endblock %}
```

#### Flask Templating:
To be added soon!

## When to Use

Consider using the Presenter pattern when your application requires:

- Complex data aggregation from multiple models
- Significant presentation-specific transformations
- Consolidated validation across multiple models
- Improved separation of concerns

## Advanced Features

- Error collection and merging
- Complex data transformations
- Presentation-specific computations and formatting

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](https://choosealicense.com/licenses/mit/) file for details.

## Acknowledgments

Inspired by architectural patterns that emphasize separation of concerns.

## Mentions

Many thanks to [JetBrains](https://www.jetbrains.com/?from=python-presenter) for supplying me with a license to use their product in the development
of this tool.

![JetBrains](readme-data/jetbrains.svg)
