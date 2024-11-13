from flask import render_template, request, jsonify
from app import app, db
from models import Context, GeneratedFile
from utils.openrouter import generate_code
from utils.code_generator import process_generation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        requirements = data.get('requirements')
        specifications = data.get('specifications')
        
        if not requirements:
            return jsonify({'error': 'Requirements are required'}), 400
            
        context = Context(
            title=data.get('title', 'Untitled Project'),
            requirements=requirements,
            specifications=specifications,
            status='processing'
        )
        db.session.add(context)
        db.session.commit()
        
        # Generate code using OpenRouter.ai
        generated_response = generate_code(requirements, specifications)
        
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
            'error_message': context.error_message
        },
        'files': [{
            'path': file.file_path,
            'content': file.content
        } for file in files]
    })
