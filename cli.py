import click

import simple_rsync


@click.group()
def cli():
    pass


@cli.command()
@click.argument("src")
@click.argument("dest")
@click.option("--block-len", default=1024)
@click.option("--strong-len", default=8)
def signature(src: str, dest: str, block_len: int, strong_len: int):
    simple_rsync.signature(src, dest, block_len, strong_len)


@cli.command()
@click.argument("src")
@click.argument("signature")
@click.argument("dest")
def delta(src: str, signature: str, dest: str):
    simple_rsync.delta(src, signature, dest)


@cli.command()
@click.argument("base")
@click.argument("delta")
@click.argument("dest")
def patch(base: str, delta: str, dest: str):
    simple_rsync.patch(base, delta, dest)


if __name__ == "__main__":
    cli()
