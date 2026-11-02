"""Shared form helper used by every member's forms."""
from django import forms


def bootstrap(fields):
    """Add Bootstrap classes to a set of form fields."""
    for field in fields.values():
        widget = field.widget
        css = "form-select" if isinstance(widget, forms.Select) else "form-control"
        if isinstance(widget, forms.CheckboxInput):
            css = "form-check-input"
        widget.attrs.setdefault("class", css)
