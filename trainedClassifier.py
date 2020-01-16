from StringTagger.StringClf import Classifier
from StringTagger.getPage import getTextPage

training_data = { # Datos para entrenar al clasificador
	"Musica y Danza":[
		'https://es.wikipedia.org/wiki/Categor%C3%ADa:G%C3%A9neros_musicales',
		'https://www.google.com/search?rlz=1C1CHBF_esCL841CL841&sxsrf=ACYBGNS_LqTuruNJluHMQbZPvo4SD0AYZA:1579144720259&ei=ENYfXpC0D-WG0AaVyJv4CA&q=eventos+musica&oq=eventos+infantiles&gs_l=psy-ab.3..0l10.77755.80435..80595...0.7..1.195.1321.15j3......0....1..gws-wiz.......0i71j35i39j0i131j0i67j0i20i263j0i131i67j0i3.lgumpqCWYIY&uact=5&ibp=htl;events&rciv=evn#fpstate=tldetail&htivrt=events&htidocid=fxBZB2DPE70mWIrkJpA8-A%3D%3D',
		'https://www.google.com/search?rlz=1C1CHBF_esCL841CL841&sxsrf=ACYBGNS_LqTuruNJluHMQbZPvo4SD0AYZA:1579144720259&ei=ENYfXpC0D-WG0AaVyJv4CA&q=eventos+baile&oq=eventos+infantiles&gs_l=psy-ab.3..0l10.77755.80435..80595...0.7..1.195.1321.15j3......0....1..gws-wiz.......0i71j35i39j0i131j0i67j0i20i263j0i131i67j0i3.lgumpqCWYIY&uact=5&ibp=htl;events&rciv=evn#fpstate=tldetail&htivrt=events&htidocid=34Y2nzDS7gFT8hE-z_fnTg%3D%3D'

	],
	"Deportes":[
		'https://es.wikipedia.org/wiki/Categor%C3%ADa:Deportes_Ol%C3%ADmpicos_de_Verano',
		'https://es.wikipedia.org/wiki/Categor%C3%ADa:Deportes_Ol%C3%ADmpicos_de_Invierno',
		'https://www.google.com/search?rlz=1C1CHBF_esCL841CL841&sxsrf=ACYBGNS_LqTuruNJluHMQbZPvo4SD0AYZA:1579144720259&ei=ENYfXpC0D-WG0AaVyJv4CA&q=eventos+deportes&oq=eventos+infantiles&gs_l=psy-ab.3..0l10.77755.80435..80595...0.7..1.195.1321.15j3......0....1..gws-wiz.......0i71j35i39j0i131j0i67j0i20i263j0i131i67j0i3.lgumpqCWYIY&uact=5&ibp=htl;events&rciv=evn#fpstate=tldetail&htivrt=events&htidocid=bUtyX3NsTmYhL6EpJpA8-A%3D%3D'
	],
	"Cine y Teatro":[
		'https://www.google.com/search?rlz=1C1CHBF_esCL841CL841&sxsrf=ACYBGNS_LqTuruNJluHMQbZPvo4SD0AYZA:1579144720259&ei=ENYfXpC0D-WG0AaVyJv4CA&q=eventos+cine&oq=eventos+infantiles&gs_l=psy-ab.3..0l10.77755.80435..80595...0.7..1.195.1321.15j3......0....1..gws-wiz.......0i71j35i39j0i131j0i67j0i20i263j0i131i67j0i3.lgumpqCWYIY&uact=5&ibp=htl;events&rciv=evn#fpstate=tldetail&htivrt=events&htidocid=xvPBKbQL1uHWZtHYk_qgRA%3D%3D',
		'https://www.google.com/search?rlz=1C1CHBF_esCL841CL841&sxsrf=ACYBGNS_LqTuruNJluHMQbZPvo4SD0AYZA:1579144720259&ei=ENYfXpC0D-WG0AaVyJv4CA&q=eventos+teatro&oq=eventos+infantiles&gs_l=psy-ab.3..0l10.77755.80435..80595...0.7..1.195.1321.15j3......0....1..gws-wiz.......0i71j35i39j0i131j0i67j0i20i263j0i131i67j0i3.lgumpqCWYIY&uact=5&ibp=htl;events&rciv=evn#fpstate=tldetail&htivrt=events&htidocid=futJvJDZDVUkXt__JpA8-A%3D%3D'

	],
	"Museo y Parques":[
		'https://es.wikipedia.org/wiki/Anexo:Museos_de_Chile',
		'https://es.wikipedia.org/wiki/Anexo:Parques_nacionales_de_Chile',
		'https://www.google.com/search?q=eventos+museos&rlz=1C1CHBF_esCL841CL841&oq=eventos+museos&aqs=chrome..69i57j0l7.10881j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwij1vTXlofnAhVeIrkGHSz-BTcQ5rwDKAF6BAgKEAw#htivrt=events&htidocid=kXUl9qNJzkI6zoABJpA8-A%3D%3D&fpstate=tldetail'
	],
	"Ciencia y Negocios":[
		'https://www.google.com/search?rlz=1C1CHBF_esCL841CL841&sxsrf=ACYBGNRNDa21uAlUoLhPsNLr1lQHsVUA_w:1579139933531&ei=XcMfXvCGIKDA5OUP0OCFqAI&q=eventos+ciencia&oq=eventos+ciencia&gs_l=psy-ab.3..35i39j0l5j0i22i30l4.20351.22157..22447...0.4..0.105.833.10j1......0....1..gws-wiz.......0i71.5GOv3wVxZus&uact=5&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwjBuNzhgofnAhXjHbkGHTijAFUQ5rwDKAF6BAgQEAw#htivrt=events&htidocid=Oa8agiOcBPLdGuZsJpA8-A%3D%3D&fpstate=tldetail',
		'https://www.google.com/search?rlz=1C1CHBF_esCL841CL841&sxsrf=ACYBGNRNDa21uAlUoLhPsNLr1lQHsVUA_w:1579139933531&ei=XcMfXvCGIKDA5OUP0OCFqAI&q=eventos+negocios&oq=eventos+ciencia&gs_l=psy-ab.3..35i39j0l5j0i22i30l4.20351.22157..22447...0.4..0.105.833.10j1......0....1..gws-wiz.......0i71.5GOv3wVxZus&uact=5&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwjBuNzhgofnAhXjHbkGHTijAFUQ5rwDKAF6BAgQEAw#fpstate=tldetail&htivrt=events&htidocid=P0slvGL_A-rFg6K8JpA8-A%3D%3D'
	],
	"Infantil y Familia":[
		'https://www.google.com/search?rlz=1C1CHBF_esCL841CL841&sxsrf=ACYBGNS_LqTuruNJluHMQbZPvo4SD0AYZA:1579144720259&ei=ENYfXpC0D-WG0AaVyJv4CA&q=eventos+infantiles&oq=eventos+infantiles&gs_l=psy-ab.3..0l10.77755.80435..80595...0.7..1.195.1321.15j3......0....1..gws-wiz.......0i71j35i39j0i131j0i67j0i20i263j0i131i67j0i3.lgumpqCWYIY&uact=5&ibp=htl;events&rciv=evn#htivrt=events&htidocid=0Lr6CrrMDAHIpQkSk_qgRA%3D%3D&fpstate=tldetail'
	] 
}

clf = Classifier() # Instancia del clasificador

for category,urls in training_data.items(): # Entrenamos al clasificador con el contenido de cada pagina
	for url in urls:
		clf.train(getTextPage(url),category) # El metodo "getTextPage", recibe como argumento una url para extraer su texto


