from dataclasses import dataclass

from environs import Env


@dataclass
class HostSettings:
    domain_name: str

@dataclass
class DjangoSettings:
    debug: bool
    secret_key: str


@dataclass
class StripeSettings:
    secret_key: str
    published_key: str


@dataclass
class Config:
    django: DjangoSettings
    stripe: StripeSettings
    host: HostSettings


def load_config() -> Config:
    env = Env()
    env.read_env()
    return Config(
        django=DjangoSettings(
            debug=env.bool('DEBUG'), secret_key=env.str('SECRET_KEY')
        ),
        stripe=StripeSettings(
            secret_key=env.str('STRIPE_SECRET_KEY'),
            published_key=env.str('STRIPE_PUBLISHED_KEY'),
        ),
        host=HostSettings(
            domain_name=env.str('DOMAIN_NAME')
        )
    )


config: Config = load_config()
