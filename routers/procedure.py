from datetime import date

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from models.doctor import Doctor
from models.procedure import (
    FinancialReport,
    GlossedReport,
    NewProcedure,
    Procedure,
    ProcedureDetail,
)
from models.user import User

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

# TODO ADD AUTH, VALIDATION, ERROR HANDLING

USER_AUTH = User()


@router.post("/registry", response_model=ProcedureDetail)
async def create_procedure(
    procedure: NewProcedure,
    current_user: dict = Depends(USER_AUTH.get_current_user),
) -> ProcedureDetail:
    """
    Create a new procedure.

    @JSON Params:\n
        - doctor_id: ID of the doctor\n
        - patient_id: ID of the patient\n
        - date: Date of the procedure\n
        - value: Value of the procedure\n
        - payment_status: Payment status of the procedure (paid, pending, glossed)\n

    @Return:\n
        - ProcedureDetail: Details of the created procedure\n
            * id: ID of the procedure\n
            * doctor_id: ID of the doctor\n
            * patient_id: ID of the patient\n
            * date: Date of the procedure\n
            * value: Value of the procedure\n
            * payment_status: Payment status of the procedure (paid, pending, glossed)\n
    """
    # if superuser, enable insetion withou checking doctor id
    if current_user.is_superuser:
        if not procedure.doctor_id or not procedure.patient_id:
            return JSONResponse(
                status_code=400,
                content={"message": "Doctor and patient IDs are required."},
            )

        db_procedure = Procedure(**procedure.model_dump())
        db_procedure.create()
        return db_procedure

    # is not a doctor
    if not Doctor.exists(user_id=current_user.id):
        return JSONResponse(
            status_code=400,
            content={"message": "Doctor not found."},
        )

    # change procedure ID to the current doctor ID
    procedure.doctor_id = Doctor.get_by_user_id(user_id=current_user.id).id
    db_procedure = Procedure(**procedure.model_dump())
    db_procedure.create()
    return db_procedure


@router.get("/report/daily", response_model=list[ProcedureDetail])
async def get_daily_report(
    doctor_id: int | None = None,
    current_user: dict = Depends(USER_AUTH.get_current_user),
) -> list[ProcedureDetail]:
    """
    Get daily report of procedures by doctor.
    """
    current_doctor = Doctor.get_by_user_id(user_id=current_user.id)

    # if super user, check if is a doctor or selected some doctor
    if current_user.is_superuser:
        if not doctor_id and not current_doctor:
            return JSONResponse(
                status_code=400,
                content={"message": "Doctor is required."},
            )

        if not doctor_id:
            doctor_id = current_doctor.id
        return Procedure.filter(date=date.today(), doctor_id=doctor_id)

    if not current_doctor:
        return JSONResponse(
            status_code=404,
            content={"message": "Doctor not found."},
        )

    return Procedure.filter(date=date.today(), doctor_id=current_doctor.id)


@router.post("/report/glossed", response_model=list[ProcedureDetail])
async def get_glossed_report(
    data: GlossedReport,
    current_user: dict = Depends(USER_AUTH.get_current_user),
) -> list[ProcedureDetail]:
    """
    Get glossed report of procedures by period.
    """
    return Procedure.filter(
        date__range=(data.start, data.end), payment_status="glossed"
    )


@router.get("/report/financial/{doctor_id}", response_model=list[FinancialReport])
async def get_financial_report(
    doctor_id: int,
    current_user: dict = Depends(USER_AUTH.get_current_user),
) -> list[FinancialReport]:
    """
    Get financial report of procedures by doctor.

    @JSON Params:\n
        - doctor_id: ID of the doctor\n

    @Return:\n
        - FinancialReport: Financial report of the doctor\n
            * total_value: Total value of the procedures\n
            * procedures: Number of procedures\n
            * status: Status of the payment (paid, pending, glossed)\n
    """
    return Procedure.get_financial_report(doctor_id=doctor_id)
