from odoo import api, fields, models
from odoo.exceptions import UserError


class PrestamoEquipo(models.Model):
    _name = "prestamo.equipo"
    _description = "Equipo para préstamo"
    _order = "name"

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código de inventario", required=True, copy=False)
    categoria = fields.Selection(
        [
            ("laptop", "Laptop"),
            ("proyector", "Proyector"),
            ("audio", "Audio"),
            ("laboratorio", "Laboratorio"),
        ],
        string="Categoría",
        required=True,
        default="laptop",
    )
    estado = fields.Selection(
        [
            ("disponible", "Disponible"),
            ("prestado", "Prestado"),
            ("mantenimiento", "En mantenimiento"),
        ],
        string="Estado",
        required=True,
        default="disponible",
        group_expand=True,
    )
    notas = fields.Text(string="Notas")
    active = fields.Boolean(string="Activo", default=True)
    veces_prestado = fields.Integer(
        string="Veces prestado", compute="_compute_veces_prestado"
    )

    _sql_constraints = [
        ("codigo_equipo_unico", "unique(codigo)", "El código de inventario debe ser único."),
    ]

    def _compute_veces_prestado(self):
        Linea = self.env["prestamo.linea"]
        for equipo in self:
            equipo.veces_prestado = Linea.search_count([("equipo_id", "=", equipo.id)])

    def action_enviar_mantenimiento(self):
        for equipo in self:
            if equipo.estado == "prestado":
                raise UserError("No se puede enviar a mantenimiento un equipo prestado.")
            equipo.estado = "mantenimiento"

    def action_marcar_disponible(self):
        for equipo in self:
            if equipo.estado == "prestado":
                raise UserError("Un equipo prestado no puede marcarse como disponible.")
            equipo.estado = "disponible"
