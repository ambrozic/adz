import click

from adz import ADZ, CFG, Echo

CTX = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CTX, help="ADZ command line interface")
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file path")
@click.option("--details", "-d", is_flag=True, help="Show endpoint details from config")
@click.option("--list", "-l", "list_", is_flag=True, help="List endpoints from config")
@click.option("--output", "-o", is_flag=True, help="Show parsed config")
@click.option("--settings", "-s", is_flag=True, help="Show settings from config")
@click.option("--var", "-v", multiple=True, help="Pass or override variables to config")
@click.option("--colors/--no-colors", default=None, help="Control color output")
@click.option("--response/--no-response", default=None, help="Hide response in output")
@click.argument("endpoints", type=str, nargs=-1, required=False)
def main(config, details, list_, output, settings, var, colors, response, endpoints):
    config = CFG.configure(
        path=config,
        settings=dict(colors=colors, response=response),
        variables=dict([v.split("=", 1) for v in var]),
    )
    if not config:
        return print("Missing configuration file")

    adz = ADZ(config=config)
    echo = Echo(config=config)

    if list_:
        echo()
        echo("  » Endpoints")
        for name, values in config.endpoints.items():
            echo(f"    • {name}\t{values.get('description', '')}")
        return echo()

    if settings:
        echo()
        echo("  » Settings")
        for k, v in config.settings.items():
            echo(f"    • {k}: {v}")
        echo()
        echo(f"  From config file at '{config.path}'")
        return echo()

    if output:
        echo("  » Configuration")
        echo(config.to_dict(), "json")
        return echo()

    for endpoint in endpoints:
        if endpoint not in config.endpoints:
            echo()
            echo(f'"{endpoint}" endpoint does not exist')
            echo()
            continue

        if details:
            echo()
            echo(f'  » Endpoint "{endpoint}"')
            for name, values in config.endpoints[endpoint].items():
                echo(f"    • {name}\t{values}")
            echo()
            continue

        response = adz(name=endpoint)
        echo(f"{response.method} " f"{response.url}")
        echo(f"{response.http_version} {response.status_code} {response.status_phrase}")

        for k, v in response.headers.items():
            echo(f" • {k}: {v if 'auth' not in k.lower() else '<hidden>'}")

        if config.settings["response"]:
            echo()
            echo(response.content, "json")
        echo()

    if not endpoints:
        with click.Context(main) as ctx:
            echo(main.get_help(ctx))
