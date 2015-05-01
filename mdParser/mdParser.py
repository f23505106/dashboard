from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

class MdExtension(Extension):
	def extendMarkdown(self, md, md_globals):
# Insert code here to change markdown's behavior.
		print(type(md.inlinePatterns))
