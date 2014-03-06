# -*- coding: utf-8 -*-
from django import template
from django.db.models import get_model
from django.template.loader import render_to_string

from favit.models import Favorite


register = template.Library()

@register.filter
def get_favorite_for(obj, user):
    """
    Get Favorite instance for an object (obj) and a user (user)

    Usage:
    {% with obj|get_favorite_for:user as fav_object %}
        ...
    {% endwith %}
    """

    return Favorite.objects.get_favorite(user, obj)


@register.filter
def favorites_count(obj):
    """
    Usage:

    Given an object `obj` you may show it fav count like this:

    <p>Favorite Count {{ obj|favorites_count }}</p>
    """

    return Favorite.objects.for_object(obj).count()


@register.assignment_tag
def favorites(obj):
    """
    Usage:

    {% favorites obj as favorite_list %}
      {% for fav_obj in favorite_list %}
	  {# do something with fav_obj #}
      {% endfor %}
    """
    return Favorite.objects.for_object(obj)


@register.assignment_tag
def user_favorites(user, app_model=None):
    """
    Usage:

    Get all user favorited objects:

        {% with user_favorites <user> as favorite_list %}
            {% for fav_obj in favorite_list %}
                {# do something with fav_obj #}
            {% endfor %}
        {% endwith %}

    or, just favorites from one model:

        {% with user_favorites <user> "app_label.model" as favorite_list %}
            {% for fav_obj in favorite_list %}
                {# do something with fav_obj #}
            {% endfor %}
        {% endwith %}
    """

    return Favorite.objects.for_user(user, app_model)


@register.assignment_tag
def model_favorites(app_model):
    """
    Gets all favorited objects that are instances of a model
    given in module notation.

    Usage:

        {% with model_favorites "app_label.model" as favorite_list %}
            {% for fav_obj in favorite_list %}
                {# do something with fav_obj #}
            {% endfor %}
        {% endwith %}
    """

    return Favorite.objects.for_model(app_model)
