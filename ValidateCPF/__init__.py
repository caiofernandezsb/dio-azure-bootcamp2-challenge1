import azure.functions as func
import json
import re

def is_valid_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)  

    if len(cpf) != 11 or cpf in [str(i) * 11 for i in range(10)]:
        return False

    def calcular_digito(cpf_parcial, peso):
        soma = sum(int(digit) * peso for digit, peso in zip(cpf_parcial, range(peso, 1, -1)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    primeiro_digito = calcular_digito(cpf[:9], 10)
    segundo_digito = calcular_digito(cpf[:10], 11)

    return cpf[-2:] == primeiro_digito + segundo_digito

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        cpf = req_body.get('cpf', '')

        if not cpf:
            return func.HttpResponse(json.dumps({"error": "CPF is required"}), status_code=400, mimetype="application/json")

        is_valid = is_valid_cpf(cpf)

        return func.HttpResponse(
            json.dumps({"cpf": cpf, "valid": is_valid}),
            status_code=200,
            mimetype="application/json"
        )
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")
