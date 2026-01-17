# -*- coding: utf-8 -*-

from odoo import models, fields

class ReportDataWizard(models.TransientModel):
    """
    Este es un modelo transitorio (un 'wizard') que actúa como un
    intermediario estable entre el menú y la acción del informe.
    """
    _name = 'report.data.wizard'
    _description = 'Asistente para Informe de Datos Externos'

    def action_print_report(self):
        """
        Este método es llamado por el botón 'Imprimir' del wizard.
        Llama a la acción de informe original y la devuelve, lo que
        le indica a la interfaz de Odoo que descargue el PDF.
        """
        # Se asegura de que la llamada al informe se hace en un contexto limpio
        # y bien definido, iniciado por el usuario.
        return self.env.ref('mi_modulo_informes.action_report_external_data').report_action()
