import numpy as np


class Payment:
    def __init__(self, when, payment):
        self.when = when
        self.payment = payment

    def resolve(self, pmt):
        """

        :param pmt: payments array
        :return:
        """

        if isinstance(self.when, dict):
            ix = slice(int(self.when['from']) - 1, int(self.when['to']) - 1)    # because config numbers starts from 1
        else:
            ix = slice(int(self.when) - 1, int(self.when))      # same

        this_payment = np.zeros(pmt.shape)
        if isinstance(self.payment, dict):
            this_payment[ix] -= pmt[ix]     # because pmt are negative numbers but up_to is positive number
            this_payment[ix] -= float(self.payment['up_to'])
        else:
            this_payment[ix] -= float(self.payment)

        return this_payment
