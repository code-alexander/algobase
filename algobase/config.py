"""Configuration settings for the algobase."""

from dynaconf import Dynaconf, Validator

from algobase.choices import AlgorandNetwork

settings = Dynaconf(
    envvar_prefix="AB",  # Abbreviation for 'algobase'
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    load_dotenv=True,
    env_switcher="AB_ENV",
    validators=[
        Validator(
            "ALGORAND_NETWORK",
            when=Validator("NAME", eq="") | Validator("NAME", eq="dev"),
            default=AlgorandNetwork.LOCALNET,
        ),
        Validator(
            "ALGORAND_NETWORK",
            when=Validator("NAME", eq="test"),
            default=AlgorandNetwork.TESTNET,
        ),
        Validator(
            "ALGORAND_NETWORK",
            when=Validator("NAME", eq="prod"),
            default=AlgorandNetwork.MAINNET,
        ),
        Validator(
            "ALGORAND_NETWORK",
            condition=lambda x: x in AlgorandNetwork._value2member_map_,
            messages={
                "condition": "{name} configuration invalid in {env} environment. Found '{value}' but expected 'localnet', 'testnet', or 'mainnet'.",
            },
        ),
        Validator("ALGORAND_NETWORK", cast=AlgorandNetwork),
        Validator(
            "ALGOD_TOKEN",
            when=Validator("ALGORAND_NETWORK", eq="localnet"),
            default="a" * 64,
        ),
        Validator("ALGOD_TOKEN", cast=str),
    ],
)
