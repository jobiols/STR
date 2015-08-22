# -*- coding: utf-8 -*-
#################################################################################

from datetime import datetime, timedelta

from openerp.osv import fields, osv


class curso_lapse(osv.osv):
    """ Define un lapso de tiempo se usa como clase abstracta """
    _name = 'curso.lapse'
    _description = __doc__

    #   def _check_elapsed(self, cr, uid, ids, context=None):
    #        for curso in self.browse(cr, uid, ids, context=context):
    #            if curso.date_end < curso.date_begin:
    #                return False
    #        return True

    def _elapsed_time(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for rec in self.browse(cr, uid, ids):
            res[rec.id] = rec.end_time - rec.start_time
        return res

    _columns = {
        'start_time': fields.float('Desde', required=True),
        'end_time': fields.float('Hasta', required=True),
        'elapsed_time': fields.function(_elapsed_time, string="Duración", type="float",
                                        method=True)
    }


class curso_holiday(osv.osv):
    """ define los periodos donde estamos en vacaciones, puede ser parte de un dia """
    _name = 'curso.holiday'
    _inherit = 'curso.lapse'

    _columns = {
        'name': fields.char('Nombre', size=64, required=False, readonly=False),
        'date': fields.date('Fecha'),
    }

    _defaults = {
        'start_time': 8,
        'end_time': 22,
    }


class curso_schedule(osv.osv):
    """ horarios que puede tener un curso """
    _name = 'curso.schedule'
    _inherit = 'curso.lapse'

    def _f2h(self, t):
        mm = t - int(t)
        hh = t - mm
        return "{:0>2d}:{:0>2d}".format(int(hh), int(mm * 60))

    def _f2hh_mm(self, t):
        mm = t - int(t)
        hh = t - mm
        mm *= 60
        if int(mm) == 0:
            res = "{}hs".format(int(hh))
        else:
            res = "{}hs {}min".format(int(hh), int(mm))
        return res

    def _get_name(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for shedule in self.browse(cr, uid, ids, context=context):
            aa = self._f2h(shedule.start_time)
            bb = self._f2h(shedule.end_time)
            cc = self._f2hh_mm(shedule.end_time - shedule.start_time)
            name = "{} - {} ({})".format(aa, bb, cc)
            res[shedule.id] = name
        return res

    _columns = {
        'name': fields.function(_get_name, fnct_search=None, string='Nombre del horario',
                                method=True, store=True,
                                type='char'),
    }

    _sql_constraints = [
        ('default_code_unique', 'unique (name)', 'Este horario ya existe.')]


class curso_lecture(osv.osv):
    """ Representa las clases del curso """
    _description = __doc__
    _name = 'curso.lecture'

    def _weekday(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for rec in self.browse(cr, uid, ids):
            ans = datetime.strptime(rec.date, '%Y-%m-%d')
            res[rec.id] = ans.strftime("%A")
        return res

    def _calc_datetime(self, _date, _time):

        dt = datetime.strptime(_date, "%Y-%m-%d")

        mm = _time - int(_time)
        hh = int(_time - mm)
        mm = int(mm * 60)

        tt = datetime(dt.year, dt.month, dt.day, hh, mm, tzinfo=None)

        # TODO aca sumamos tres horas porque inexplicablemente al mostrar el campo le resta tres horas.
        tt = tt + timedelta(hours=3)
        b = tt.strftime("%Y-%m-%d %H:%M:%S")

        return b

    def _get_start(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for rec in self.browse(cr, uid, ids):
            res[rec.id] = self._calc_datetime(rec.date, rec.schedule_id.start_time)
        return res

    def _get_stop(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for rec in self.browse(cr, uid, ids):
            res[rec.id] = self._calc_datetime(rec.date, rec.schedule_id.end_time)
        return res

    _columns = {
        'date': fields.date('Fecha'),
        'desc': fields.text('Descripcion'),
        'curso_id': fields.many2one('curso.curso', 'Curso', readonly=False,
                                    required=True),
        'schedule_id': fields.many2one('curso.schedule', 'Horario', readonly=False,
                                       required=True),
        'weekday': fields.function(_weekday, string="Dia", type="char", method=True),
        'date_start': fields.function(_get_start, string="Inicio de clase",
                                      type="datetime", method=True),
        'date_stop': fields.function(_get_stop, string="Fin de clase", type="datetime",
                                     method=True),
    }


class curso_quota(osv.osv):
    def _get_state(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for quota in self.browse(cr, uid, ids, context=context):
            res[quota.id] = 'Pendiente'
            register_pool = self.pool.get('account.invoice')
            if quota.invoice_id:
                records = register_pool.search(cr, uid,
                                               [('id', '=', quota.invoice_id.id)])
                for reg in register_pool.browse(cr, uid, records, context):
                    if reg.state == 'draft':
                        res[quota.id] = 'Borrador'
                    if reg.state == 'paid':
                        res[quota.id] = 'Pagado'
                    if reg.state == 'open':
                        res[quota.id] = 'Abierto'
                    if reg.state == 'cancel':
                        res[quota.id] = 'Cancelado'
        return res

    def _get_amount_paid(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for quota in self.browse(cr, uid, ids, context=context):
            res[quota.id] = 0
            register_pool = self.pool.get('account.invoice')
            if quota.invoice_id:
                records = register_pool.search(cr, uid,
                                               [('id', '=', quota.invoice_id.id)])
                for reg in register_pool.browse(cr, uid, records, context):
                    res[quota.id] = reg.amount_total
        return res

    """ Curso Quota """
    _name = 'curso.quota'
    _description = __doc__
    _columns = {
        'registration_id': fields.many2one('curso.registration', 'Inscripcion'),
        'date': fields.date('Fecha factura'),
        'amount': fields.function(_get_amount_paid, fnct_search=None, string='Facturado',
                                  method=True, store=False,
                                  type='char'),
        'state': fields.function(_get_state, fnct_search=None, string='Estado Factura',
                                 method=True, store=False,
                                 type='char'),
        'list_price': fields.float('Precio'),
        'quota': fields.integer('#cuota', readonly=False),
        'curso_inst': fields.related('registration_id', 'curso_id', 'curso_instance',
                                     string='Instancia', type='char',
                                     size=128, readonly=True),
        'partner_id': fields.related('registration_id', 'partner_id', 'name',
                                     string='Alumna', type='char', size=128,
                                     readonly=True),
        'invoice_id': fields.many2one('account.invoice', 'Factura', required=False),
    }
    _order = 'date desc'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
