from ..db.database import get_session
from ..db.models import Control, AssessmentResult
import datetime
import click

def run_interactive_assessment():
    session = get_session()
    controls = session.query(Control).all()
    
    if not controls:
        click.echo("No controls found. Did you run 'compliancehub init'?")
        return
        
    click.echo(f"Starting assessment for {len(controls)} controls...")
    
    results = []
    for control in controls:
        click.echo(f"\n[{control.id}] {control.title}")
        click.echo(f"{control.description}")
        
        status = click.prompt("Status (Met/Partial/Not Met)", type=click.Choice(['Met', 'Partial', 'Not Met'], case_sensitive=False))
        rationale = click.prompt("Rationale", type=str)
        
        result = AssessmentResult(
            control_id=control.id,
            status=status.title(),
            rationale=rationale,
            assessed_at=datetime.datetime.now()
        )
        session.add(result)
        results.append(result)
        
    session.commit()
    click.echo("\nAssessment complete and saved!")
