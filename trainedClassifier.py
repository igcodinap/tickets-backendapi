from StringTagger.StringClf import Classifier
from StringTagger.getPage import getTextPage

training_data = { # Datos para entrenar al clasificador
	"Musica":[
		'https://www.google.com/search?q=eventos+musica&rlz=1C1CHBF_esCL841CL841&oq=eventos+danza&aqs=chrome..69i57j0l7.4183j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwiK17a1zIbnAhUOheAKHRVkDnwQ5rwDKAF6BAgKEAw#fpstate=tldetail&htivrt=events&htidocid=fxBZB2DPE70mWIrkJpA8-A%3D%3D'
	],
	"Deportes":[
		'https://www.google.com/search?q=eventos+deportes&rlz=1C1CHBF_esCL841CL841&oq=eventos+deportes&aqs=chrome..69i57j0l7.2940j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwis8JXmofzmAhXNG7kGHRfDCvMQ5rwDKAF6BAgREAw#htivrt=events&htidocid=bUtyX3NsTmYhL6EpJpA8-A%3D%3D&fpstate=tldetail'
	],
	"Cine y Teatro":[
		'https://www.google.com/search?q=eventos+teatro&rlz=1C1CHBF_esCL841CL841&oq=eventos+danza&aqs=chrome..69i57j0l7.4183j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwiK17a1zIbnAhUOheAKHRVkDnwQ5rwDKAF6BAgKEAw#fpstate=tldetail&htivrt=events&htidocid=bpYgORLx3zVd5D4aJpA8-A%3D%3D',
		'https://www.google.com/search?q=eventos+cine&rlz=1C1CHBF_esCL841CL841&oq=eventos+danza&aqs=chrome..69i57j0l7.4183j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwiK17a1zIbnAhUOheAKHRVkDnwQ5rwDKAF6BAgKEAw#fpstate=tldetail&htivrt=events&htidocid=xvPBKbQL1uHWZtHYk_qgRA%3D%3D',
	],
	"Infantil y Familia":['https://www.google.com/search?q=eventos+familiares&rlz=1C1CHBF_esCL841CL841&oq=eventos+familiares&aqs=chrome..69i57j0l7.2842j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwjcsLrtm_zmAhUqD7kGHdYQAIsQ5rwDKAF6BAgQEAw#htivrt=events&htidocid=9JUZn4jsi0xVw6LkJpA8-A%3D%3D&fpstate=tldetail',
	],
	"Museo y Parques":['https://www.google.com/search?q=eventos+museo&rlz=1C1CHBF_esCL841CL841&oq=eventos+danza&aqs=chrome..69i57j0l7.4183j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwiK17a1zIbnAhUOheAKHRVkDnwQ5rwDKAF6BAgKEAw#fpstate=tldetail&htivrt=events&htidocid=kXUl9qNJzkI6zoABJpA8-A%3D%3D',
						'https://www.google.com/search?q=eventos+parques&rlz=1C1CHBF_esCL841CL841&oq=eventos+danza&aqs=chrome..69i57j0l7.4183j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwiK17a1zIbnAhUOheAKHRVkDnwQ5rwDKAF6BAgKEAw#fpstate=tldetail&htivrt=events&htidocid=r1UiGpVSM6ABgfruJpA8-A%3D%3D'
	],
	"Danza":['https://www.google.com/search?q=eventos+danza&rlz=1C1CHBF_esCL841CL841&oq=eventos+danza&aqs=chrome..69i57j0l7.4183j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwiK17a1zIbnAhUOheAKHRVkDnwQ5rwDKAF6BAgKEAw#htivrt=events&htidocid=bpYgORLx3zVd5D4aJpA8-A%3D%3D&fpstate=tldetail'
	]

	
}

clf = Classifier() # Instancia del clasificador

for category,urls in training_data.items(): # Entrenamos al clasificador con el contenido de cada pagina
	for url in urls:
		clf.train(getTextPage(url),category) # El metodo "getTextPage", recive como argumento una url para extraer su texto


