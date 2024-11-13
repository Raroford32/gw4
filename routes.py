from flask import render_template, request, jsonify
from app import app, db
from models import Context, GeneratedFile, Template
from utils.openrouter import generate_code
from utils.code_generator import process_generation
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        templates = Template.query.filter_by(is_active=True).all()
        logger.info(f"Retrieved {len(templates)} templates from database")
        for template in templates:
            logger.info(f"Template: {template.name} (ID: {template.id})")
        return render_template('index.html', templates=templates)
    except Exception as e:
        logger.error(f"Error retrieving templates: {str(e)}")
        return render_template('index.html', templates=[])


@app.route('/api/templates', methods=['GET'])
def list_templates():
    templates = Template.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'description': t.description
    } for t in templates])


@app.route('/api/templates', methods=['POST'])
def create_template():
    data = request.json
    if not data.get('name') or not data.get('base_prompt'):
        return jsonify({'error': 'Name and base prompt are required'}), 400

    template = Template(
        name=data['name'],
        description=data.get('description', ''),
        base_prompt=data['base_prompt']
    )
    db.session.add(template)
    db.session.commit()

    return jsonify({
        'id': template.id,
        'name': template.name,
        'description': template.description
    })


@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        message = data.get('message')
        model = data.get('model', 'grok-beta')
        template_id = data.get('template_id')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Get template if specified
        template = None
        if template_id:
            template = Template.query.get(template_id)
            if template:
                message = f"{template.base_prompt}\n\nUser Requirements:\n{message}"

        context = Context(
            title='Chat Generated Project',
            requirements=message,
            specifications='Generated via chat interface',
            status='processing',
            template_id=template_id if template else None
        )
        db.session.add(context)
        db.session.commit()

        # Generate code using OpenRouter.ai
        generated_response = generate_code(message, model)

        if generated_response.get('error'):
            context.status = 'error'
            context.error_message = generated_response['error']
            db.session.commit()
            return jsonify({'error': generated_response['error']}), 500

        # Process the generated code
        files = process_generation(generated_response['code'])

        for file_info in files:
            generated_file = GeneratedFile(
                context_id=context.id,
                file_path=file_info['path'],
                content=file_info['content']
            )
            db.session.add(generated_file)

        context.status = 'completed'
        context.generated_code = generated_response['code']
        db.session.commit()

        return jsonify({
            'status': 'success',
            'context_id': context.id,
            'files': files
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/context/<int:context_id>')
def get_context(context_id):
    context = Context.query.get_or_404(context_id)
    files = GeneratedFile.query.filter_by(context_id=context_id).all()

    return jsonify({
        'context': {
            'id': context.id,
            'title': context.title,
            'requirements': context.requirements,
            'specifications': context.specifications,
            'status': context.status,
            'error_message': context.error_message,
            'template_id': context.template_id
        },
        'files': [{
            'path': file.file_path,
            'content': file.content
        } for file in files]
    })
