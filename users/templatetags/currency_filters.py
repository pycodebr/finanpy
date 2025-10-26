import locale
from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def currency(value):
    """
    Formata valores monetários em reais (R$).

    Args:
        value: Valor numérico (int, float, Decimal) ou None

    Returns:
        String formatada como 'R$ 1.234,56'

    Examples:
        {{ 1234.56|currency }} -> 'R$ 1.234,56'
        {{ 0|currency }} -> 'R$ 0,00'
        {{ None|currency }} -> 'R$ 0,00'
    """
    # Tratar None e valores vazios
    if value is None or value == '':
        value = 0

    # Converter para Decimal para precisão
    try:
        value = Decimal(str(value))
    except (ValueError, TypeError):
        value = Decimal('0')

    # Tentar usar locale pt_BR.UTF-8
    try:
        # Salvar locale atual
        old_locale = locale.getlocale(locale.LC_MONETARY)

        # Configurar locale brasileiro
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

        # Formatar usando locale
        formatted = locale.currency(value, grouping=True, symbol=None)

        # Restaurar locale original
        locale.setlocale(locale.LC_MONETARY, old_locale)

        # Adicionar símbolo R$
        return f'R$ {formatted}'

    except locale.Error:
        # Fallback: formatação manual se locale não disponível
        # Converter para float para formatação
        float_value = float(value)

        # Separar parte inteira e decimal
        if float_value < 0:
            sign = '-'
            float_value = abs(float_value)
        else:
            sign = ''

        # Formatar com 2 casas decimais
        integer_part = int(float_value)
        decimal_part = int(round((float_value - integer_part) * 100))

        # Adicionar separadores de milhares
        integer_str = str(integer_part)
        formatted_integer = ''

        for i, digit in enumerate(reversed(integer_str)):
            if i > 0 and i % 3 == 0:
                formatted_integer = '.' + formatted_integer
            formatted_integer = digit + formatted_integer

        # Montar valor formatado
        return f'{sign}R$ {formatted_integer},{decimal_part:02d}'
