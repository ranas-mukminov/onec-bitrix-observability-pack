import click
import json
from ai_assistant.bottleneck_detector import BottleneckDetector
from ai_assistant.recommendation_engine import RecommendationEngine

@click.group()
def cli():
    pass

@cli.command()
@click.argument('snapshot_file', type=click.File('r'))
def analyze_snapshot(snapshot_file):
    """Analyze a JSON snapshot of metrics."""
    try:
        metrics = json.load(snapshot_file)
    except json.JSONDecodeError:
        click.echo("Error: Invalid JSON file.")
        return

    detector = BottleneckDetector()
    bottlenecks = detector.analyze(metrics)

    if not bottlenecks:
        click.echo("No bottlenecks detected.")
        return

    click.echo(f"Detected {len(bottlenecks)} potential bottlenecks:")
    for b in bottlenecks:
        click.echo(f"- [{b.component}] {b.reason} (Confidence: {b.confidence})")

    rec_engine = RecommendationEngine()
    recommendations = rec_engine.get_recommendations(bottlenecks)
    
    click.echo("\nRecommendations:")
    for r in recommendations:
        click.echo(f"- {r}")

if __name__ == '__main__':
    cli()
