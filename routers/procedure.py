import typing
from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

# from fastapi.responses import JSONResponse
from models.procedure import Procedure

blueprint_name = "procedure"

router = APIRouter(
    prefix=f"/{blueprint_name}",
    tags=[blueprint_name],
    responses={404: {"description": "Not found"}},
)


"""A API deve ter endpoints para:

 - Cadastrar um novo procedimento médico com os seguintes dados:
    - ID do médico
    - ID do paciente
    - Data do procedimento
    - Valor do procedimento
    - Status do pagamento (pago, pendente, glosado)
 - Gerar um relatório diário de procedimentos por médico.
 - Gerar um relatório de glosas por período.
 - Gerar um relatório financeiro por médico.


Por favor, compartilhe o link do repositório Git com o código-fonte e inclua:

 - A documentação da API (pode ser em formato Swagger).
 - Explicação de como a API lida com erros e exceções.
 - Explicação de como a API garante a segurança dos dados."""


class NewProcedure(BaseModel):
    doctor_id: int
    patient_id: int
    date: date
    value: float
    payment_status: typing.Literal["paid", "pending", "glossed"]


class ProcedureDetail(NewProcedure):
    model_config = ConfigDict(from_attributes=True)

    id: int
    doctor: str
    patient: str


@router.post("/registry", response_model=ProcedureDetail)
async def create_procedure(procedure: NewProcedure) -> ProcedureDetail:
    db_procedure = Procedure(**procedure.model_dump())
    db_procedure.save()
    return db_procedure


@router.get("/report/daily", response_model=list[ProcedureDetail])
async def get_daily_report() -> list[ProcedureDetail]:
    procedures = Procedure.create()
    return procedures
