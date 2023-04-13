from urllib import request
import re

# Spoofed user agent... because reasons
user_agent = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

news_sources = [
	('https://thehackernews.com/', 'HN'),
	('https://portswigger.net/daily-swig', 'PS'),
]

link_patterns = {
	'HN':{
		'title':"<h2 class='home-title'>.+<\/h2>",
		'link':"<a class='story-link'.*>"
	},
	'PS':{
		'title':'<span class="main">.+<\/span>',
		'link':'<a href="\/daily-swig\/.+class="noscript-post">'
	},
}

#for source in news_sources:
def get_news(source):
	url, tag = source
	
	http_request = request.Request(
		url, data=None,
		headers=user_agent,
		origin_req_host=None,
		unverifiable=False,
		method='GET'
	)

	page = request.urlopen(http_request)
	html = page.read().decode('utf-8')

	dirty_titles = re.findall(link_patterns[tag]['title'], html, re.IGNORECASE)
	dirty_links = re.findall(link_patterns[tag]['link'], html, re.IGNORECASE)

	titles = []
	links = []

	for title in dirty_titles:
		titles.append(re.sub("<.*?>", "", title))
	
	for link in dirty_links:
		s = re.findall("href=.*", link, re.IGNORECASE)[0].split(' ')[0]
		s = re.sub(">", "", s)[6:-1]
		
		if tag == 'PS':
			s = "https://portswigger.net" + s
		
		links.append(s)

	return titles, links



page_start = """<html>
<head>
<title>Cyber news</title>
</head>
<body>
<h1>Cyber News</h1>\n"""

page_end = """</body>
</html>
"""

page_body = ""

for source in news_sources:
	url, tag = source
	site = re.search(r"//.*(.net|.com)", url).group()[2:]
	
	page_body += "<h2>" + site + "</h2><hr />\n"
	
	titles, links = get_news(source)
	for i in range(len(titles)):
		page_body += "<a href='" + links[i] + "'>"
		page_body += "<h3>" + titles[i] + "</h3></a>\n"

f = open("news.html", 'w')
f.write(page_start)
f.write(page_body)
f.write(page_end)
f.close()
		
