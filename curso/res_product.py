# -*- coding: utf-8 -*-
#################################################################################

from datetime import datetime

from openerp.osv import fields, osv


def generate_html(dict):
    ret = ""
    for data in dict:
        ret += "<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\">"
        ret += "	<tbody>"
        ret += "		<tr>"
        ret += "			<td>"
        ret += "			<h2>" + data['titulo'] + "</h2>"
        ret += "			</td>"
        ret += "			<td>"
        ret += "			<h5><sub>&nbsp;cod " + data['codigo'] + "</sub></h5>"
        ret += "			</td>"
        ret += "		</tr>"
        ret += "</tbody>"
        ret += "</table>"

        ret += "<p>" + data['acerca_de'] + "</p>"
        ret += "<p>Duracion " + data['duracion_semanas'] + " semanas, (" + data['horas_catedra'] + "hs)<br/>"
        ret += "Modalidad " + data['modalidad'] + "</p>"

        ret += "<table  border=\"0\" cellpadding=\"1\" cellspacing=\"1\" style=\"width: 500px;\">"
        ret += "    <tbody>"
        ret += "        <tr>"
        ret += "            <td><strong>Inicio</strong></td>"
        ret += "            <td><strong>Cod</strong></td>"
        ret += "            <td><strong>Dias de cursada</strong></td>"
        ret += "            <td><strong>Horario</strong></td>"
        ret += "        </tr>"
        for line in data['cursos']:
            ret += "        <tr bgcolor=\"#E0ECF8\">"
            ret += "            <td><span style=\"font-size:14px;\">" + line['inicio'] + "</span></td>"
            ret += "            <td><span style=\"font-size:14px;\">" + line['instancia'] + "</span></td>"
            ret += "            <td><span style=\"font-size:14px;\">" + line['dias'] + "</span></td>"
            ret += "            <td><span style=\"font-size:14px;\">" + line['horario'] + "</span></td>"
            ret += "        </tr>"

        ret += "    </tbody>"
        ret += "</table>"
        ret += "<br>"
        if data['temario']:
            ret += "<h2>Temario</h2>"
            ret += data['temario']

    ret += "<br>"
    ret += "<table border=\"0\" cellpadding=\"1\" cellspacing=\"1\" style=\"width: 100%;\">"
    ret += "	<tbody>"
    ret += "		<tr>"
    ret += "			<td>"
    ret += "			<h3 style=\"text-align: center;\">Se entrega certificado</h3>"
    ret += "			<p style=\"text-align: center;\"><img alt=\"\" src=\"https://d3njjcbhbojbot.cloudfront.net/web/images/promos/cdp_cert_logo.png\" style=\"width: 110px; height: 110px;\" /></p>"
    ret += "			<p style=\"text-align: center;\">Materiales inclu&iacute;dos en el costo del curso.</p>"
    ret += "			</td>"
    ret += "		</tr>"
    ret += "</tbody>"
    ret += "</table>"
    ret += "<br>"
    ret += "<h2>Aranceles</h2>"
    ret += "<table border=\"0\" cellpadding=\"1\" cellspacing=\"1\" style=\"width: 500px;\">"
    ret += "	<tbody>"
    for data in dict:
        ret += "		<tr>"
        ret += "			<td>"
        ret += "			   <p>" + data['codigo'] + " " + data['titulo'] + "</p>"
        ret += "			</td>"
        ret += "			<td>"

        if data['cuotas'] == '1':
            ss = data['cuotas'] + " cuota de $" + data['valor']
        else:
            ss = data['cuotas'] + " cuotas de $" + data['valor'] + " c/u"

        ret += "			   <p>Matr&iacute;cula: " + data['matricula'] + " - " + ss + "</p>"
        ret += "			</td>"
        ret += "		</tr>"
    ret += "</tbody>"
    ret += "</table>"
    return ret


class product_product(osv.osv):
    _inherit = 'product.product'  # Permite la herencia propiamente dicho del modulo product
    _columns = {
        'tot_hs_lecture': fields.integer('Horas catedra', help="Cantidad de horas que tiene el curso en total."),
        'classes_per_week': fields.integer('Clases por semana', help="Cantidad de clases en la semana."),
        'hs_lecture': fields.integer('Horas de clase', help="Duración de cada una de las clases."),
        'agenda': fields.text('Tema'),
        'no_quotes': fields.integer('Cantidad de cuotas'),

        'default_reply_to': fields.char('Respuesta por defecto', size=64,
                                        help="El mail del organizador, que se pondra en el campo de respuesta de todos los mails enviados automaticamente en inscripciones y confirmaciones de cursos."),
        'default_email_registration': fields.many2one('email.template', 'Mail de inscripcion',
                                                      help="Selecciona el mail de inscripcion que se enviara a la alumna"),
        'default_email_curso': fields.many2one('email.template', 'Mail de confirmacion',
                                               help="Selecciona el mail de confirmacion que se enviara a la alumna en el momento de la confirmacion"),
        'default_registration_min': fields.integer('Minimo de alumnas en el curso',
                                                   help="define la cantidad minima de alumnas para arrancar el curso. (Pone cero para no tener en cuenta la regla)"),
        'default_registration_max': fields.integer('Maximo de alumnas en el curso',
                                                   help="Define la cantidad maxima de alumnas que puede tener el curso. (Pone cero para no tener en cuenta la regla)"),
    }
    _defaults = {
        'default_registration_min': 0,
        'default_registration_max': 0,
        'classes_per_week': 1,
        'no_quotes': 1,
        'default_reply_to': "makeoverlabinfo@gmail.com"
    }

    #    _sql_constraints = [('default_code_unique', 'unique (default_code)', 'ya hay un producto con esta referencia.')]
    def wd2day(self, wd):
        dict = {
            '0': 'Lunes',
            '1': 'Martes',
            '2': 'Miercoles',
            '3': 'Jueves',
            '4': 'Viernes',
            '5': 'Sabado',
            '6': 'Domingo'}
        return dict[wd]

    def generate_doc(self, cr, uid, ids, context=None):
        for prod in self.browse(cr, uid, ids, context=context):

            cursos = []
            if not prod.description:
                prod.description = ""

            instance_pool = self.pool.get('curso.curso')
            records = instance_pool.search(cr, uid,
                                           [('default_code', '=', prod.default_code), ('state', '!=', 'cancel')])
            for inst in instance_pool.browse(cr, uid, records, context=context):
                schedule = ""
                if inst.schedule_1:
                    schedule = inst.schedule_1.name

                cursos.append({'inicio': datetime.strftime(datetime.strptime(inst.date_begin, '%Y-%m-%d'), '%d/%m/%Y'),
                               'instancia': '{}/{:0>2d}'.format(prod.default_code, inst.instance),
                               'dias': self.wd2day(inst.weekday_1),
                               'horario': schedule,
                               })
            try:
                weeks = str((prod.tot_hs_lecture / prod.hs_lecture) / prod.classes_per_week)
            except:
                weeks = "error!"

            data = {
                'titulo': prod.name,
                'codigo': prod.default_code,
                'acerca_de': prod.description,
                'duracion_semanas': weeks,
                'horas_catedra': str(prod.tot_hs_lecture),
                'modalidad': str(prod.classes_per_week) + ' clase de ' + str(prod.hs_lecture) + ' hs por semana',
                'cursos': cursos,
                'temario': prod.agenda,
                'matricula': 'Bonificada',
                'cuotas': str(prod.no_quotes),
                'valor': str(prod.list_price),
            }

            new_page = {
                'name': prod.name,
                'content': generate_html([data]),
            }

        # Borrar el documento si es que existe
        doc_pool = self.pool.get('document.page')
        records = doc_pool.search(cr, uid, [('name', '=', prod.name)])
        doc_pool.unlink(cr, uid, records)

        # Crear el documento
        self.pool.get('document.page').create(cr, uid, new_page, context=context)

        return True
