from dependency_injector import containers, providers

from app.db import get_session
from app.domain.repositories.CallRepository import CallRepository
from app.domain.repositories.UserRepository import UserRepository


class AppContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])

    db_session = providers.Resource(get_session)

    call_repository: providers.Factory[CallRepository] = providers.Factory(
        CallRepository, db_session
    )

    user_repository: providers.Factory[UserRepository] = providers.Factory(
        UserRepository, db_session
    )
