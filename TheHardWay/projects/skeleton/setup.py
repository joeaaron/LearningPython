try:
	from setuptools impot setup
except ImportError:
	from distutils.core impot setup

config = {
	'description': 'My Project',
	'autor':'My name',
	'url': 'URL to get it at.',
	'download_url':'Where to download it.',
	'author_email':'My email',
	'version':'0.1',
	'install_requires':['nose'],
	'packages':['NAME'],
	'scripts':[]
	'name':'projectname'
}

setup(**config)