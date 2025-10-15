try:
    from dash import dcc, html
except ImportError:
    import dash_core_components as dcc
    import dash_html_components as html

__all__ = ['dcc', 'html']