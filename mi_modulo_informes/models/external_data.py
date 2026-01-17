# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ExternalData(models.AbstractModel):
    _name = 'external.data'
    _description = 'Modelo Virtual para Datos de Informe'
    _auto = False

    # El campo 'id' o 'record_id' se elimina. El ORM gestionará el ID.
    nombre = fields.Char('Nombre del Registro', readonly=True)
    total = fields.Float('Valor Total', readonly=True)

    @api.model
    def _get_report_data(self, docids, data=None):
        """
        Esta función es llamada por la acción de informe para recolectar
        los datos que se enviarán a la plantilla QWeb.
        """
        # Ya no necesitamos definir 'record_id' aquí.
        report_data_dicts = [
            {'nombre': 'Registro de Ejemplo 1', 'total': 150.75},
            {'nombre': 'Registro de Ejemplo 2', 'total': 89.99},
            {'nombre': 'Registro de Ejemplo 3', 'total': 345.00},
            {'nombre': 'Registro de Ejemplo 4', 'total': 120.50},
        ]

        docs = self.env[self._name].new(report_data_dicts)

        return {
            # Usamos los IDs reales (temporales) de los registros creados.
            'doc_ids': docs.ids,
            'doc_model': self._name,
            'docs': docs,
            'company': self.env.company,
        }
