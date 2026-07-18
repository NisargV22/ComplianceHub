import click
import os
import datetime
from jinja2 import Environment, FileSystemLoader
from .generator import generate_gap_assessment
from ..db.database import get_session
from ..db.models import RiskFinding, Control

@click.group(name='report')
def report_cli():
    """Generate reports."""
    pass

@report_cli.command(name='gap-assessment')
@click.option('--output', default='gap_report.html', help='Output HTML filename')
def gap_assessment(output):
    """Generate a gap assessment HTML report."""
    click.echo(f"Generating gap assessment report: {output}")
    generate_gap_assessment(output)
    click.echo("Done.")

@report_cli.command(name='risk-register')
@click.option('--output', default='risk_register.html', help='Output HTML filename')
def risk_register(output):
    """Generate a risk register HTML report."""
    click.echo(f"Generating risk register report: {output}")
    session = get_session()
    results = session.query(RiskFinding).all()
    
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('risk_register.html.j2')
    
    html_out = template.render(
        results=results,
        generated_date=datetime.datetime.now().strftime("%Y-%m-%d")
    )
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html_out)
    click.echo("Done.")

@report_cli.command(name='policy')
@click.option('--template', required=True, help='Template name (e.g. password_policy)')
@click.option('--controls', help='Comma-separated control IDs to link')
@click.option('--output', default='policy.html', help='Output HTML filename')
def policy(template, controls, output):
    """Generate a policy document HTML."""
    click.echo(f"Generating policy document: {output}")
    session = get_session()
    linked_controls = controls.split(',') if controls else []
    control_objs = session.query(Control).filter(Control.id.in_(linked_controls)).all()
    
    import markdown
    
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'policy', 'templates')))
    jinja_template = env.get_template(f"{template}.md.j2")
    
    md_out = jinja_template.render(
        controls=control_objs,
        generated_date=datetime.datetime.now().strftime("%Y-%m-%d")
    )
    
    html_out = markdown.markdown(md_out)
    html_out = f"<html><body>{html_out}</body></html>"
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html_out)
    click.echo("Done.")
