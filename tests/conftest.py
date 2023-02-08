from pytest_factoryboy import register

from tests.factories import VacancyFactory, UserFactory

# Fixtures
pytest_plugins = "tests.fixtures"

# Factories
register(VacancyFactory)
register(UserFactory)
