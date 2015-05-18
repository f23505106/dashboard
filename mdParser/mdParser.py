from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern
from markdown.preprocessors import Preprocessor
import re

class MdExtension(Extension):
	def extendMarkdown(self, md, md_globals):
		md.registerExtension(self)
		fenced = FencedBlockPreprocessor()
		md.preprocessors.add('fencedBlockPreprocessor', fenced, '_begin')
		md.parser.blockprocessors.pop('code')

class FencedBlockPreprocessor(Preprocessor):
	FENCE_BEGIN_RE = re.compile(r'^\s*`{3,}(?P<lang>[a-z]+)\s*$') #eg begin:```lang-cpp
	FENCE_END_RE   = re.compile(r'^\s*`{3,}\s*$')
	CODE_WRAP_HEADER = '<pre class="prettyprint lang-%s linenums">'
	#lang- support list  http://google-code-prettify.googlecode.com/svn/trunk/README.html
	#"bsh", "c", "cc", "cpp", "cs", "csh", "cyc", "cv", "htm", "html",
	#"java", "js", "m", "mxml", "perl", "pl", "pm", "py", "rb", "sh",
	#"xhtml", "xml", "xsl".
	CODE_WRAP_END    = '</pre>'
	
	def run(self, lines):
	#	print('input')
	#	for line in lines:
	#		print(line)

		codeBlockFlag = False
		block = []
		for line in lines:
			#print(line)
			if codeBlockFlag:
				if self.FENCE_END_RE.search(line):
					#print("fenced end tag")
					codeBlockFlag = False
					block.append(self.CODE_WRAP_END)
				else:
					#print("fenced in")
					block.append(line)
			else:
				m = self.FENCE_BEGIN_RE.search(line)
				if m:
					#print("fenced begin tag")
					codeBlockFlag = True
					lang = (m.group('lang') or None)
					block.append(self.CODE_WRAP_HEADER % (lang))
				else:
					block.append(line)
		
		if codeBlockFlag:
			codeBlockFlag = False
			block.append(self.CODE_WRAP_END)
		#print('output')
		#for line in block:
		#	print(line)
		return block


