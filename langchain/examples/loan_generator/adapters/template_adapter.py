from services.template_service import render_docx_from_template

def render_docx(template_id, context):
    return render_docx_from_template(template_id, context)