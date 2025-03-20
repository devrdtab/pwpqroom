from datetime import datetime

def get_current_date():
    """Возвращает текущую дату в формате ДД-ММ-ГГГГ ЧЧ:ММ:СС"""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def get_current_year():
    """Возвращает текущий год"""
    return datetime.now().year