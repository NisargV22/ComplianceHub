import click
import json
import os
from .db.database import init_db, get_session
from .db.models import Control
from .assessment.engine import run_interactive_assessment
from .risk.register import risk_cli
from .report.cli import report_cli

@click.group()
def cli():
    pass

cli.add_command(risk_cli)
cli.add_command(report_cli)

@cli.command()
@click.option('--framework', default='cis-v8', help='Framework to initialize')
@click.option('--company', help='Company name')
def init(framework, company):
    """Initialize the database with a framework."""
    init_db()
    session = get_session()
    
    # Check if controls already exist
    if session.query(Control).count() == 0:
        framework_file = os.path.join(os.path.dirname(__file__), 'frameworks', 'cis_v8.json')
        with open(framework_file, 'r') as f:
            data = json.load(f)
            
        for item in data:
            control = Control(
                id=item['id'],
                framework=item['framework'],
                title=item['title'],
                description=item['description'],
                domain=item['domain']
            )
            session.add(control)
        session.commit()
        click.echo(f"Seeded {len(data)} controls from {framework}.")
        
    click.echo(f"Database initialized for {company or 'unknown'} with framework {framework}")

@cli.command()
@click.option('--interactive', is_flag=True, help='Run interactive assessment')
def assess(interactive):
    """Run an assessment."""
    if interactive:
        run_interactive_assessment()
    else:
        click.echo("Please use --interactive for now.")

if __name__ == '__main__':
    cli()
