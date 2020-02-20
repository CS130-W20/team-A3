"""
__init__.py
====================
The initialization file for the visualization module
"""
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
import json

CONCEPT_PATH = "concept_hierarchy.json"