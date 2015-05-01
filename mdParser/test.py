#!/usr/bin/env python
import markdown
from mdParser import MdExtension
markdown.markdownFromFile("test.md", extensions=[MdExtension()])
