from fastapi import Request

def get_model(request:Request):
    return request.app.state.model

def get_model_config(request:Request):
    return request.app.state.config_model