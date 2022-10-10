"""
serve module implements the commands for running the
functionality of the necdfella REST API.
"""
import click


@click.command("serve")
def serve():
    """
    Run a web server with the netcdfella REST API.
    """
    click.echo("Sorry, serve functionality has not been implemente yet.")
