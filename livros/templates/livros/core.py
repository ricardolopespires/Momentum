from datetime import datetime









class Livros(object):


	def __init__(self, url):

		HEADERS = ({

			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
			'Accept-Language': 'en-US, en;q=0.5'
			})

		webpage = requests.get(url, headers=HEADERS)
		soup = BeautifulSoup(webpage.content, "lxml")
     


	def portugues(self,soup):
		try:
			titulo = soup.find("span",attrs={"id": 'productTitle'}).string.strip().replace(',', '')	     
		except AttributeError:
		    titulo = "NA"
		try:
		    descricao = soup.find("div", id =( 'bookDescription_feature_div')).find('span').string.strip()
		         
		except AttributeError:
		    descricao = "NA"	     

		try:
		    preco = soup.find("span", attrs={'class': 'a-size-base a-color-secondary'}).string.strip().replace('R$', '')
		except AttributeError:
		    preco = "NA"

		try:
		    img = soup.find("img", attrs={'class': 'image-stretch-vertical'})['src']
		except AttributeError:
		    img = "NA"

		try:
		    paginas = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[0].find('span').string.strip()
		except AttributeError:
		    paginas = "NA"

		try:
		    idioma = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[1].find('span').string.strip()
		except AttributeError:
		    idioma = "NA"

		try:
		    editora = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[2].find('span').string.strip()
		except AttributeError:
		    editora = "NA"

		try:
		    publicacao = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[3].find('span').string.strip()
		except AttributeError:
		    publicacao = "NA"

		try:
		    isbn = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[7].find('span').string.strip()
		except AttributeError:
		    isbn = "NA"  
		try:
		    autor = soup.find("a", class_=('a-size-large a-link-normal')).find('h2').string.strip()
		except AttributeError:
		    autor = "NA"

		return {

		'titulo':titulo,'descricao':descricao,
		'preco':preco,'img':img,'paginas':paginas,
		'idioma':idioma,'editora':editora,
		'publicacao':publicacao,'isbn':isbn,
		'autor':autor,


		}  




	def ingles(self, soup):
		try:
			titulo = soup.find("span",attrs={"id": 'productTitle'}).string.strip().replace(',', '')	     
		except AttributeError:
		    titulo = "NA"
		try:
		    descricao = soup.find("div", id =( 'bookDescription_feature_div')).find('span').string.strip()
		         
		except AttributeError:
		    descricao = "NA"	     

		try:
		    preco = soup.find("span", attrs={'class': 'a-size-base a-color-secondary'}).string.strip().replace('R$', '')
		except AttributeError:
		    preco = "NA"

		try:
		    img = soup.find("img", attrs={'class': 'image-stretch-vertical'})['src']
		except AttributeError:
		    img = "NA"

		try:
		    paginas = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[0].find('span').string.strip()
		except AttributeError:
		    paginas = "NA"

		try:
		    idioma = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[1].find('span').string.strip()
		except AttributeError:
		    idioma = "NA"

		try:
		    editora = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[2].find('span').string.strip()
		except AttributeError:
		    editora = "NA"

		try:
		    publicacao = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[3].find('span').string.strip()
		except AttributeError:
		    publicacao = "NA"

		try:
		    isbn = soup.find_all("div", class_=('a-section a-spacing-none a-text-center rpi-attribute-value'))[7].find('span').string.strip()
		except AttributeError:
		    isbn = "NA"  
		try:
		    autor = soup.find("a", class_=('a-size-large a-link-normal')).find('h2').string.strip()
		except AttributeError:
		    autor = "NA"

		return {

		'titulo':titulo,'descricao':descricao,
		'preco':preco,'img':img,'paginas':paginas,
		'idioma':idioma,'editora':editora,
		'publicacao':publicacao,'isbn':isbn,
		'autor':autor,


		}  





if __name__ == "__main__":

    url = "https://www.amazon.com.br/Investing-101-essential-profitable-portfolio/dp/1440595135/"

    livro = Livro()
    search = livro.portugues(url)
    print(search)

