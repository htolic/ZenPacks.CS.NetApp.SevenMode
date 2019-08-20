#!/usr/bin/env python


class Utils(object):

    def _delta(self, a2, a1):
        return a2 - a1

    def _rate(self, a2, a1, t2, t1):
        if (t2 == t1):
            return 0.
        return self._delta(a2, a1) / self._delta(t2, t1)

    def _average(self, a2, a1, b2, b1):
        return self._rate(a2, a1, b2, b1)

    def _percent(self, a2, a1, b2, b1):
        return 100 * self._average(a2, a1, b2, b1)
