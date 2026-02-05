# Main Page Toctree (for cross-references)
```{toctree}
:maxdepth: 1
:caption: Main Page

README
```
# NOTE: This file (index.md) is used as the main landing page for Sphinx documentation.
# It includes the project README.md as the main content using the MyST include directive below.
# This approach ensures that the README.md is rendered as the main page, with all Markdown formatting and links preserved.
#
# Do NOT use index.rst for the main page if you want Markdown/MyST features—Sphinx will always prioritize index.rst over index.md if both exist.
#
# The toctree directives below provide navigation for API reference and project documents.
```{include} README.md
```


```{toctree}
:maxdepth: 2
:caption: API Reference

io/llm/utils
io/llm/openai
io/llm/genai
io/llm/deepseek
io/llm/logging_utils
io/read_data
```

```{toctree}
:maxdepth: 1
:caption: Project Documents

ROADMAP.md
CHANGE_LOG.md
CODE_OF_CONDUCT.md
SETUP_GUIDE.md
CONTRIBUTORS.md
LICENSE.md
```

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
