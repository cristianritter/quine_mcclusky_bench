from time import perf_counter

from quine_mccluskey.qm import QuineMcCluskey


class TimedQuineMcCluskey(QuineMcCluskey):
    """Subclass of QuineMcCluskey that records timing for phase 1 and phase 2.

    Phase 1: generation of prime implicants.
    Phase 2: selection of essential implicants and further reduction.
    """

    def simplify_los(self, ones, dc=None, num_bits=None):
        if dc is None:
            dc = []

        self.profile_cmp = 0
        self.profile_xor = 0
        self.profile_xnor = 0

        terms = set(ones) | set(dc)
        if len(terms) == 0:
            self.time_phase1 = 0.0
            self.time_phase2 = 0.0
            return None

        if num_bits is not None:
            self.n_bits = num_bits
        else:
            self.n_bits = max(len(i) for i in terms)
            if self.n_bits != min(len(i) for i in terms):
                self.time_phase1 = 0.0
                self.time_phase2 = 0.0
                return None

        # Phase 1: generate prime implicants
        t0 = perf_counter()
        prime_implicants = self._QuineMcCluskey__get_prime_implicants(terms)
        t1 = perf_counter()

        # Phase 2: essential implicants and final reduction
        essential_implicants = self._QuineMcCluskey__get_essential_implicants(
            prime_implicants, set(dc)
        )
        reduced_implicants = self._QuineMcCluskey__reduce_implicants(
            essential_implicants, set(dc)
        )
        t2 = perf_counter()

        self.time_phase1 = t1 - t0
        self.time_phase2 = t2 - t1

        return reduced_implicants
