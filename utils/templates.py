"""Project templates configuration and management."""

templates = {
    'web': {
        'name': 'Web Application',
        'description': 'Create a web application with routing, templates, and database integration',
        'base_prompt': '''Create a web application with:
- Frontend using HTML/CSS/JavaScript
- Backend routing and controllers
- Database models and integration
- Form handling and validation
- Error handling and logging'''
    },
    'api': {
        'name': 'REST API',
        'description': 'Build a RESTful API with proper structure and documentation',
        'base_prompt': '''Create a REST API with:
- Proper endpoint structure
- Input validation
- Error handling
- Database integration
- API documentation'''
    },
    'cli': {
        'name': 'Command Line Tool',
        'description': 'Develop a command-line interface application',
        'base_prompt': '''Create a CLI application with:
- Command-line argument parsing
- Input validation
- Error handling
- Progress indicators
- Help documentation'''
    }
}

def get_template(template_id):
    """Get a template by its ID."""
    return templates.get(template_id)

def get_all_templates():
    """Get all available templates."""
    return [{'id': tid, **tdata} for tid, tdata in templates.items()]

def get_template_prompt(template_id, user_requirements):
    """Combine template base prompt with user requirements."""
    template = get_template(template_id)
    if not template:
        return user_requirements
    
    return f"""{template['base_prompt']}

Additional Requirements:
{user_requirements}"""
