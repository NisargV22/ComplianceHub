from jinja2 import Environment, FileSystemLoader
import os
import datetime
from ..db.database import get_session
from ..db.models import Control, AssessmentResult

def generate_gap_assessment(output_path):
    session = get_session()
    results = session.query(AssessmentResult).all()
    controls = session.query(Control).all()
    
    # Simple mapping
    control_map = {c.id: c for c in controls}
    
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('gap_assessment.html.j2')
    
    html_out = template.render(
        results=results,
        control_map=control_map,
        generated_date=datetime.datetime.now().strftime("%Y-%m-%d")
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_out)
    return output_path
