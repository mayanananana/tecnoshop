# -*- coding: utf-8 -*-

from odoo import models, fields

class ReportDataWizard(models.TransientModel):
    _name = 'report.data.wizard'
    _description = 'Asistente para Informe de Datos Externos'

    def action_print_report(self):
        """
        Este método ahora busca todos los registros del modelo 'external.data'
        (que provienen de la vista SQL) y pasa sus IDs al informe.
        """
        # Buscamos todos los registros en la vista.
        records = self.env['external.data'].search([])
        if not records:
            # Opcional: manejar el caso de que la vista esté vacía.
            return

        # Pasamos los IDs de los registros encontrados al informe.
        return self.env.ref('mi_modulo_informes.action_report_external_data').report_action(docids=records.ids)