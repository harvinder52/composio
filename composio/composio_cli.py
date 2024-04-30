#!/usr/bin/env python3

import argparse
import os
from cloup import HelpFormatter, HelpTheme, Style, command, option, option_group

from rich.console import Console

from cloup.constraints import RequireAtLeast, mutually_exclusive

formatter_settings = HelpFormatter.settings(
    theme=HelpTheme(
        invoked_command=Style(fg='bright_yellow'),
        heading=Style(fg='bright_white', bold=True),
        constraint=Style(fg='magenta'),
        col1=Style(fg='bright_yellow'),
    )
)

@command(formatter_settings=formatter_settings)
def main():
    """Main entry point for Composio CLI."""
    console = Console()
    console.print("Welcome to Composio CLI", style="bold green")

@command(formatter_settings=formatter_settings)
@option_group(
    "Cool options",
    option('--foo', help='This text should describe the option --foo.'),
    option('--bar', help='This text should describe the option --bar.'),
    constraint=mutually_exclusive,
)
def run(foo, bar):
    """Run the main functionality with exclusive options."""
    console = Console()
    console.print("Running main function with options:", style="bold green")
    if foo:
        console.print(f"--foo was set to: {foo}", style="italic yellow")
    if bar:
        console.print(f"--bar was set to: {bar}", style="italic yellow")

@command(formatter_settings=formatter_settings)
@option_group(
    "Login options",
    option('--foo', help='This text should describe the option --foo.'),
    constraint=mutually_exclusive,
)
def login(foo):
    """Login to Composio"""
    console = Console()
    console.print("Attempting to login...", style="bold blue")
    if foo:
        console.print(f"Login with --foo option: {foo}", style="italic magenta")
    else:
        console.print("No login options provided.", style="italic red")
