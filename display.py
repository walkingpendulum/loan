from tabulate import tabulate

import parsers


def schedule(indexer, ppmt, ipmt, principal):
    """

    :param indexer: months indexes array. will be used as index
    :param ppmt: principal payments array
    :param ipmt: interest payments array
    :param principal: principal (still-to-pay amount) array
    :return:
    """
    table = tabulate(
        zip(indexer + 1, ppmt + ipmt, ppmt, ipmt, principal),
        headers=['month', 'payment', 'principal payment', 'interest payment', 'principal'],
        tablefmt='orgtbl',
    )

    print(table)


def title(params):
    loan_period_str = params['loan_period']
    loan_period = int(parsers.parse_period(loan_period_str))
    loan_amount = int(params['loan_amount'])
    interest_rate = float(params['interest_rate'])

    print(
        f'What is the amortization schedule for '
        f'a {loan_period_str} ({loan_period} months) loan '
        f'of ₽{int(loan_amount)} at {round(100 * interest_rate, 2)}% interest '
        f'per year compounded monthly?'
    )