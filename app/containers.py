from dependency_injector import containers, providers

from app.db import get_session
from app.domain.repositories.CallRepository import CallRepository
from app.domain.repositories.InvoiceRepository import InvoiceRepository
from app.domain.repositories.UserRepository import UserRepository
from app.domain.services import InvoiceService
from app.domain.services.billing import FlatRatePostpaidPlanStrategy


class AppContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])

    db_session = providers.Resource(get_session)

    call_repository: providers.Factory[CallRepository] = providers.Factory(
        CallRepository, db_session
    )

    invoice_repository: providers.Factory[
        InvoiceRepository
    ] = providers.Factory(InvoiceRepository, db_session)

    user_repository: providers.Factory[UserRepository] = providers.Factory(
        UserRepository, db_session
    )

    flat_rate_postpaid_strategy: providers.Factory[
        FlatRatePostpaidPlanStrategy
    ] = providers.Factory(
        FlatRatePostpaidPlanStrategy,
        tax_rate=config.default.tax_rate,
        charge_per_minute=config.billing.postpaid.charge_per_minute,
    )

    invoice_service: providers.Factory[InvoiceService] = providers.Factory(
        InvoiceService,
        billing_strategy=flat_rate_postpaid_strategy,
        call_repository=call_repository,
        invoice_repository=invoice_repository,
    )
