import numpy as np

import display
import parsers


def calc_loan_params(loan_period, loan_amount, interest_rate):
    per = np.arange(loan_period)
    ipmt = np.ipmt(interest_rate / 12, per, loan_period, loan_amount)
    ppmt = np.ppmt(interest_rate / 12, per, loan_period, loan_amount)
    return ipmt, ppmt


def main(params):
    loan_period_str = params['loan_period']
    loan_period = int(parsers.parse_period(loan_period_str))
    loan_amount = int(params['loan_amount'])
    interest_rate = float(params['interest_rate'])
    extra_payments = parsers.parse_extra_payments(params.get('extra_payments', []))

    ipmt_init, ppmt_init = calc_loan_params(
        loan_period=loan_period,
        loan_amount=loan_amount,
        interest_rate=interest_rate,
    )
    principal_init = np.zeros(loan_period) + loan_amount + np.cumsum(ppmt_init)

    pmt = ipmt_init + ppmt_init
    epmt = np.sum([e.resolve(pmt) for e in extra_payments], axis=0)
    extra_payment_happens_at = list(np.nonzero(epmt)[0])

    ipmt, ppmt, principal = ipmt_init, ppmt_init, principal_init
    for ind in extra_payment_happens_at:
        ppmt[ind] += epmt[ind]
        principal[ind] += epmt[ind]
        if principal[ind] < 0:
            ipmt = ipmt[:ind+1]
            ppmt = ppmt[:ind+1]
            principal = principal[:ind+1]
            loan_period = ind
            break

        period = int(np.nper(interest_rate / 12, pmt[ind], principal[ind]))
        _, ppmt_last = calc_loan_params(
            loan_period=period,
            loan_amount=principal[ind],
            interest_rate=interest_rate,
        )
        ppmt = ppmt[:ind + ppmt_last.shape[0]]
        principal = principal[:ind + ppmt_last.shape[0]]

        ppmt[ind:] = ppmt_last
        principal[ind:] = np.zeros(period) + principal[ind] + np.cumsum(ppmt_last)

    display.title(params)
    display.schedule(np.arange(loan_period), ppmt, ipmt, principal)


if __name__ == '__main__':
    args = parsers.arg_parser().parse_args()
    params = parsers.parse_config(args.config_path)

    main(params)
