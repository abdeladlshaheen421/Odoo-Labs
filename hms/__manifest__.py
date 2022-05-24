{
    "name":"HMS",
    "description":"this is a test odoo project",
    "depends":["crm"],
    "data":[
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/hms_patient_view.xml',
        'views/hms_department_view.xml',
        'views/hms_doctor_view.xml',
        'views/hms_customer_view.xml',
        'reports/hms_templates.xml',
        'reports/hms_reports.xml',
        
    ]
}