# -*- coding: utf-8 -*-
{
    'name' : 'Registro y Actualización de Pacientes',
    'version' : '1.0',
    'summary': 'Permite realizar el registro, búsqueda y actualización de los datos de pacientes',
    'sequence': 30,
    'description': """
Este módulo agrega datos al modelo res.partner para que se pueda utilizar para
el registro de pacientes. Siendo res.partner un módulo genérico se extiende
para reutilizarlo con otros recursos.
    """,
    'category': 'Medical',
    'website': 'https://www.vauxoo.com',
    'images' : [],
    'depends' : ['base'],
    'data': [
        'views/patient_menu.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
