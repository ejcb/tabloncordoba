# -*- coding: utf-8 -*-
import scrapy
import datetime

class ScraptablonSpider(scrapy.Spider):
    name = 'scraptablon'
    allowed_domains = ['mezquita.ayuncordoba.es']

    def start_requests(self):
        start_urls = [ 'http://mezquita.cordoba.es/atencionciudadana/oactablon.nsf/wfTablonWeb' ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tablon = response.xpath('//*["EventoEnlace"]')
        dict_anuncio = {}
        lista_enlaces = []
        lista_textos = []
        base_enlace = 'http://mezquita.cordoba.es/atencionciudadana/oactablon.nsf/'

        # recopila enlaces
        for anuncio in tablon.xpath('@href'):
            enlace_anuncio = base_enlace + anuncio.get()
            lista_enlaces.append( enlace_anuncio )

        # Elimina de los enlaces los elementos no pertinentes (no son anuncios pero comparten xpath)
        lista_enlaces.remove( base_enlace + '/atencionciudadana/oactablon.nsf/pFormularios.css' )
        lista_enlaces.remove( base_enlace + '/atencionciudadana/oactablon.nsf/pEstilos.css' )

        # recopila textos
        for anuncio in tablon.xpath('a/text()'):
            texto_anuncio = anuncio.get()
            lista_textos.append( texto_anuncio )

        # mezcla listas en un dictionary
        mezcla_listas = zip( lista_enlaces, lista_textos )
        dict_anuncio = dict ( mezcla_listas )
        for clave, valor in dict_anuncio.iteritems():
            yield {
                    "fecha_captura": datetime.datetime.now().replace(microsecond=0).isoformat(),
                    "enlace": clave,
                    "texto": valor,
                   }

