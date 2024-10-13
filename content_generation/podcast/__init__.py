import tomli

with open("config.toml", "rb") as f:
    config = tomli.load(f)

config = config["podcast"]
