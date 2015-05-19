#!/usr/bin/env python
import web
import codecs
import markdown
from collections import OrderedDict
import os
import time
from mdParser import MdExtension

# URLs: map everything to the page class
urls = (
	'/index(.html)?', 'Index',
	'/about(.html)?', 'About',
	'/contact(.html)?', 'Contact',
	'/post(.html)?', 'Post',
	'/(.*)', 'page',
)

# Templates are found in the templates directory
render = web.template.render('templates')

# Application
app = web.application(urls, globals())

# Markdown
md = markdown.Markdown(extensions=[MdExtension()])

class page:
	def GET(self, url):
		# Handle index pages: path/ maps to path/index.txt
		if url == "" or url.endswith("/"):
			url += "index"

		# Each URL maps to the corresponding .txt file in pages/
		page_file = 'pages/%s.md' %(url)

		# Try to open the text file, returning a 404 upon failure
		try:
			f = codecs.open(page_file,mode= 'r',encoding="utf-8")
		except IOError:
			return web.notfound()

		# Read the entire file, converting Markdown content to HTML
		content = f.read()
		content = md.convert(content)
		mainHead="untitle"
		secondHead=""
		f.seek(0)
		line = f.readline()
		while line:
			line=line.strip()
			if line.startswith("##"):
				secondHead=line[2:]
			elif line.startswith("#"):
				mainHead=line[1:]
			elif line:
				break
			line = f.readline()
		f.close()

		# Render the page.html template using the converted content
		html = render.blog(mainHead,secondHead,time.ctime(os.path.getmtime(page_file)),content)
		#html = render.blog("123")
		#print(html)

		return html
#used to generate index blog list page
class Index:
	def GET(self, url):
		mdDir="pages"
		listResult=""
		mainHead="untitle"
		secondHead=""
		itemTemplate="""
		<div class="post-preview">
			<a href="%s">
				<h2 class="post-title">
				%s
				</h2>
				<h3 class="post-subtitle">
				%s
				</h3>
			</a>
			<p class="post-meta">Last modify %s</p>
		</div>
		<hr/>
		"""
		mdDict={}
		for root,dirs,files in os.walk(mdDir):
			for f in files:
				if f.endswith(".md"):
					path=os.path.join(root,f)
					mdDict[path]=os.path.getmtime(path)
		mdDict=OrderedDict(sorted(mdDict.items(),key=lambda t:t[1],reverse=True))
		#print(mdDict)
		for f,t in mdDict.items():
			fd=open(f,"r")
			line = fd.readline()
			while line:
				line=line.strip()
				if line.startswith("##"):
					secondHead=line[2:]
				elif line.startswith("#"):
					mainHead=line[1:]
				elif line:
					break
				line = fd.readline()
			fd.close()
			listResult+=itemTemplate%(os.path.basename(f)[:-3],mainHead,secondHead,time.ctime(t))
			mainHead="untitle"
			secondHead=""
		#print(listResult)
		#static web pass
		#raise web.seeother("./static/html/index.html")
		return	render.index(listResult)

#about page
class About:
	def GET(self, url):
		return	render.about()
class Contact:
	def GET(self, url):
		return	render.contact()
class Post:
	def GET(self, url):
		return	render.post()

if __name__ == '__main__':
	app.run()
