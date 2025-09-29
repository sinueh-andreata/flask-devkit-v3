import re
from flask import jsonify

def cpfValidator(cpf):
    if not cpf or not cpf.strip():
        return jsonify({"error": "CPF é obrigatório"}), 400
        
    cpf = re.sub(r'[^\d]', '', cpf) 
    if not re.match(r'^\d{11}$', cpf):
        return jsonify({"error": "CPF deve ter 11 dígitos numéricos"}), 400

    if cpf == cpf[0] * 11:
        return jsonify({"error": "CPF inválido"}), 400

    def calc_digito(cpf_parcial, fator):
        soma = 0
        for i in range(len(cpf_parcial)):
            soma += int(cpf_parcial[i]) * (fator - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calc_digito(cpf[:9], 10)
    digito2 = calc_digito(cpf[:9] + str(digito1), 11)

    if cpf[-2:] == f"{digito1}{digito2}":
        return True
    else:
        return jsonify({"error": "CPF inválido"}), 400


def validar_email(email):
    if not email or not email.strip():
        return jsonify({"error": "Email é obrigatório"}), 400
        
    email = email.strip()
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({"error": "Email inválido"}), 400
    return True


def validar_cnpj(cnpj):
    if not cnpj or not cnpj.strip():
        return jsonify({"error": "CNPJ é obrigatório"}), 400
        
    cnpj = re.sub(r'[^\d]', '', cnpj)
    if not re.match(r'^\d{14}$', cnpj):
        return jsonify({"error": "CNPJ deve ter 14 dígitos numéricos"}), 400

    if cnpj == cnpj[0] * 14:
        return jsonify({"error": "CNPJ inválido"}), 400

    def calc_digito(cnpj_parcial, pesos):
        soma = sum(int(cnpj_parcial[i]) * pesos[i] for i in range(len(cnpj_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1

    digito1 = calc_digito(cnpj[:12], pesos1)
    digito2 = calc_digito(cnpj[:12] + str(digito1), pesos2)

    if cnpj[-2:] == f"{digito1}{digito2}":
        return True
    else:
        return jsonify({"error": "CNPJ inválido"}), 400


def validar_numero_celular(num_celular):
    if not num_celular or not num_celular.strip():
        return jsonify({"error": "Número de celular é obrigatório"}), 400
        
    num_celular = re.sub(r'[^\d]', '', num_celular)

    if len(num_celular) != 11:
        return jsonify({"error": "Celular deve ter 11 dígitos"}), 400

    # Validar DDD (deve estar entre 11 e 99)
    ddd = int(num_celular[:2])
    if ddd < 11 or ddd > 99:
        return jsonify({"error": "DDD inválido"}), 400

    if num_celular[2] != '9':
        return jsonify({"error": "Celular deve começar com 9 após o DDD"}), 400
    return True


def validar_numero_fixo(num_fixo):
    if not num_fixo or not num_fixo.strip():
        return jsonify({"error": "Número de telefone fixo é obrigatório"}), 400
        
    num_fixo = re.sub(r'[^\d]', '', num_fixo)

    if len(num_fixo) != 10:
        return jsonify({"error": "Telefone fixo deve ter 10 dígitos"}), 400

    # Validar DDD (deve estar entre 11 e 99)
    ddd = int(num_fixo[:2])
    if ddd < 11 or ddd > 99:
        return jsonify({"error": "DDD inválido"}), 400
        
    return True


def validar_cep(cep):
    if not cep or not cep.strip():
        return jsonify({"error": "CEP é obrigatório"}), 400
        
    cep_limpo = re.sub(r'[^\d]', '', cep)
    
    if len(cep_limpo) != 8:
        return jsonify({"error": "CEP deve ter 8 dígitos"}), 400
    
    return True


def passwordValidator(senha):
    if not senha:
        return jsonify({"error": "Senha é obrigatória"}), 400
        
    if len(senha) < 8:
        return jsonify({"error": "Senha deve ter pelo menos 8 caracteres"}), 400
    if not re.search(r'[A-Z]', senha):
        return jsonify({"error": "Senha deve conter ao menos uma letra maiúscula"}), 400
    if not re.search(r'[a-z]', senha):
        return jsonify({"error": "Senha deve conter ao menos uma letra minúscula"}), 400
    if not re.search(r'\d', senha):
        return jsonify({"error": "Senha deve conter ao menos um número"}), 400
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return jsonify({"error": "Senha deve conter ao menos um caractere especial"}), 400
    return True

