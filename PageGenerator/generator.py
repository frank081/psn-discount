#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
from itertools import groupby
import json
import os

from jinja2 import Environment, FileSystemLoader


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", required=True, help="Source json file")
    parser.add_argument("-t", "--target", required=True, help="Target markdown file")
    return parser.parse_args()


def _load_games(game_path):
    with open(game_path) as game_json:
        return json.load(game_json)


def _sort_games(games):
    def _calculate_discount(game):
        game["discount"] = (game["origin_price"] - game["ps_plus_price"]) / game["origin_price"] \
            if not game["origin_price"] == 0 else 0
        return game

    sorted_games = sorted(map(_calculate_discount, games),
                          key=lambda game: (game["discount"], -game["buy_price"]),
                          reverse=True)
    return sorted_games


def _render_games_template(domains):
    template_env = Environment(
        autoescape=False,
        loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")),
        trim_blocks=True
    )
    template_env.filters["markdown_escape"] = lambda mark: mark.replace("(", "%28").replace(")", "%29")

    return template_env.get_template("games.md").render({
        "domains": domains,
        "update_time": datetime.date.today().strftime("%Y-%m-%d")
    })


def _save_markdown(markdown, markdown_path):
    with open(markdown_path, "w") as markdown_file:
        markdown_file.write(markdown)


def main():
    args = _parse_args()
    games = _load_games(args.source)
    domains = [
        {
            "name": domain,
            "games": _sort_games(list(domain_games))
        }
        for domain, domain_games
        in groupby(sorted(games, key=lambda game: game["domain"]), lambda game: game["domain"])]
    markdown = _render_games_template(domains)
    _save_markdown(markdown, args.target)


if __name__ == "__main__":
    main()
