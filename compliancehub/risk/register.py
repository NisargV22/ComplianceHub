import click
from ..db.database import get_session
from ..db.models import RiskFinding, Control
from .scoring import score_risk
import datetime

@click.group(name='risk')
def risk_cli():
    """Manage risk register."""
    pass

@risk_cli.command()
@click.option('--finding', required=True, help='Description of the finding')
@click.option('--control', help='Control ID this finding relates to')
@click.option('--likelihood', type=click.Choice(['low', 'medium', 'high'], case_sensitive=False), required=True)
@click.option('--impact', type=click.Choice(['low', 'medium', 'high'], case_sensitive=False), required=True)
def add(finding, control, likelihood, impact):
    """Add a risk finding to the register."""
    session = get_session()
    
    if control:
        # Validate control exists
        if not session.query(Control).filter_by(id=control).first():
            click.echo(f"Error: Control {control} not found.")
            return

    rating = score_risk(likelihood, impact)
    risk = RiskFinding(
        description=finding,
        control_id=control,
        likelihood=likelihood,
        impact=impact,
        risk_rating=rating,
        status='Open'
    )
    session.add(risk)
    session.commit()
    click.echo(f"Added Risk Finding: {rating} Risk.")

@risk_cli.command()
@click.option('--status', default='Open', help='Filter by status')
def list(status):
    """List risk findings."""
    session = get_session()
    findings = session.query(RiskFinding).filter(RiskFinding.status.ilike(status)).all()
    
    if not findings:
        click.echo("No findings found.")
        return
        
    for finding in findings:
        click.echo(f"[{finding.id}] {finding.risk_rating} Risk - {finding.description} (Control: {finding.control_id})")
