Nombre:CARLOS EDUARDO ACKERMAN ESPINOZA  
Número de cuenta:0801199723176

## Respuestas

### Paso 1. Catálogo de equipos

**1. ¿Qué pasa con un equipo cuando se desmarca el campo Activo? ¿Por qué es mejor que borrarlo?**  
El equipo queda archivado y normalmente deja de aparecer en las búsquedas y listas habituales. No se elimina de la base de datos. Es mejor archivarlo porque conserva su historial y las relaciones con préstamos anteriores, y permite reactivarlo si vuelve a utilizarse.

**2. ¿Para qué sirve `copy=False` en el campo codigo?**  
Evita que al duplicar un equipo Odoo copie automáticamente el código de inventario. Así se reduce el riesgo de que dos equipos tengan el mismo código; el nuevo registro debe recibir un código propio.

### Paso 2. Registro de préstamos

**1. Este modelo usa `_name` y `_inherit` al mismo tiempo. ¿Qué hace cada uno aquí?**  
`_name` define el nombre técnico y crea el modelo nuevo `prestamo.prestamo`. `_inherit = ["mail.thread"]` incorpora al modelo las funciones del chatter, como el historial de mensajes y el seguimiento de cambios.

**2. ¿Qué hace `tracking=True` en el campo state?**  
Activa el seguimiento del campo. Cuando cambia el estado, Odoo registra el cambio en el chatter, mostrando el valor anterior y el nuevo.

### Paso 3. Equipos del préstamo

**1. En `fields.One2many("prestamo.linea", "prestamo_id")`, ¿qué indica cada parámetro?**  
El primer parámetro, `prestamo.linea`, indica el modelo relacionado que contiene las líneas del préstamo. El segundo, `prestamo_id`, indica el campo Many2one de ese modelo que apunta al préstamo actual.

**2. ¿Qué pasa con las líneas cuando se borra un préstamo? ¿Qué parte del código lo define?**  
Las líneas relacionadas se eliminan junto con el préstamo. Lo define `ondelete="cascade"` en el campo `prestamo_id` del modelo `prestamo.linea`.

### Paso 4. Flujo de estados

**1. Los botones ya se ocultan según el estado. ¿Por qué los métodos vuelven a validar el estado?**  
Porque ocultar un botón solo controla la interfaz. La acción también puede ejecutarse desde otros medios, por ejemplo una llamada RPC o código. La validación del método protege la lógica del sistema y evita transiciones no permitidas.

**2. ¿Qué hace `prestamo.linea_ids.equipo_id.write({"estado": "prestado"})`? ¿Por qué no hace falta un `for` para cada equipo?**  
Obtiene los equipos relacionados con todas las líneas del préstamo y escribe el estado `prestado` en todos ellos. El ORM de Odoo permite ejecutar `write()` sobre un recordset completo, por eso no es necesario recorrer cada equipo manualmente.

### Paso 5. Reglas del préstamo

**1. El campo equipo_id ya filtra los equipos disponibles. ¿Por qué hace falta el TODO 5?**  
El dominio filtra las opciones que se muestran al seleccionar un equipo, pero no garantiza que el equipo siga disponible al momento de confirmar el préstamo. Otro usuario pudo cambiar su estado después de seleccionarlo. La validación en `action_prestar` vuelve a comprobarlo en el momento de prestar.

**2. ¿En qué momento se ejecuta un método con @api.constrains? ¿Y la validación de action_prestar?**  
Un método con @api.constrains se ejecuta cuando se crea o modifica un registro y cambia alguno de los campos indicados en el decorador. La validación de action_prestar se ejecuta cuando el usuario pulsa el botón Prestar y se llama ese método.

### Paso 6. Contacto, kanban y búsqueda

**1. ¿Qué pasa si arrastra una tarjeta del kanban a otra columna? ¿Por qué?**  
Como el kanban está agrupado por estado, al mover una tarjeta a otra columna Odoo puede cambiar el valor de ese campo y guardar el nuevo estado. En esta práctica no se definió una lógica que sincronice ese cambio manual con el estado de los préstamos relacionados; por eso es preferible cambiar los estados mediante los botones y reglas del flujo.

**2. El campo prestamo_ids se agregó a res.partner.**
**¿Se crea una columna nueva en la tabla de contactos? Explique.**  
No. prestamo_ids es un campo One2many inverso. Los datos de la relación se almacenan mediante el campo Many2one partner_id en la tabla del modelo prestamo_prestamo; no se necesita una columna adicional en la tabla de contactos.

## Reto implementado

- Marcar atrasado: botón visible para préstamos prestados. Solo cambia a atrasado si la fecha de devolución ya pasó.
- Colores en lista:decoration-danger para atrasados y decoration-muted para devueltos.
- Veces prestado: campo calculado que cuenta las líneas históricas asociadas al equipo.
- Mantenimiento: botones para enviar a mantenimiento y marcar disponible. No permite enviar a mantenimiento un equipo prestado.


## Repositorio
**https://github.com/careackermane-prog/practica_prestamos.git**


