# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class ExternalData(models.Model):
    """
    Este modelo ahora es un modelo de solo lectura (`_auto = False`) que mapea
    sus campos a una vista de base de datos (`_table`).
    """
    _name = 'external.data'
    _description = 'Modelo Virtual para Datos de Informe (Vista SQL)'
    _auto = False  # Impide que Odoo cree una tabla para este modelo.
    _table = 'external_data_sql_view' # Mapeamos el modelo a nuestra vista SQL.

    # Los campos ahora se corresponden directamente con las columnas de la vista SQL.
    # El campo 'id' es ahora un campo normal porque existe en la vista.
    # No lo definimos aquí porque Odoo lo gestiona implícitamente para `models.Model`.
    nombre = fields.Char('Nombre del Registro', readonly=True)
    total = fields.Float('Valor Total', readonly=True)

    @api.model
    def init(self):
        """
        El método init() se ejecuta al instalar o actualizar el módulo.
        Usamos `tools.drop_view_if_exists` para asegurar la idempotencia y
        luego creamos nuestra vista SQL.
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () AS id,
                    v.nombre,
                    v.total
                FROM (
                    VALUES
                        ('Registro de Ejemplo 1', 150.75),
                        ('Registro de Ejemplo 2', 89.99),
                        ('Registro de Ejemplo 3', 345.00),
                        ('Registro de Ejemplo 4', 120.50)
                ) AS v(nombre, total)
            )
        """ % (self._table,))