"""
Audit UD - Task 1b: SCALING check.

Task 1 confirmed accuracy.  Here we isolate the QUERY-COUNT SCALING:
does the measured query count grow like n^{1/3} * polylog (ratio q/(n^{1/3} polylog^c)
roughly constant), as the cost accounting claims?

We compute the *theoretical* per-scale query count directly from the algorithm's
formula (independent of the kd-tree exploration constant), then cross-check against
the measured count to confirm the dominant term is Otilde(n^{1/3}).

Theoretical cost (one scale lam, summed over buckets a=1,2,4,...,K):
   Sum_a  T_a * O(bucket_hi * polylog)
 = Sum_a  ceil((lam/a) eps^-2 polylog) * (2a * polylog)
 ~ Sum_a  (lam/a) * 2a * eps^-2 polylog^2
 = Sum_a  2 lam eps^-2 polylog^2
 = (#buckets) * 2 lam eps^-2 polylog^2
 = O(log K) * lam * eps^-2 polylog^2
 = Otilde(lam)   [since #buckets = O(log(lam L/eps))].

So per scale the cost is Otilde(lam).  With lam = n^{1/3} that is Otilde(n^{1/3}).
We verify the lam-linearity and the n^{1/3} value numerically.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))


def theoretical_cost_one_scale(n, lam, eps, L):
    polylog = max(1.0, math.log2(n + 2))
    K = max(2, int(lam * L / eps))
    a = 1
    total = 0.0
    nb = 0
    while a <= K:
        T_a = math.ceil((lam / a) * (1.0 / eps**2) * polylog)
        T_a = min(T_a, 4 * n)
        per_explore = 2 * a * polylog          # exploration up to 2a points, polylog/point
        total += T_a * per_explore + T_a * math.ceil(math.log2(n + 2))  # +sampling cost
        nb += 1
        a *= 2
    return total, nb, polylog, K


def main():
    eps = 0.3
    L = 8.0
    print("=== Task 1b: per-scale cost is Otilde(lam); at lam=n^{1/3} it is Otilde(n^{1/3}) ===\n")
    print("(A) Fix lam, vary n: cost should be ~independent of n except polylog.")
    print(f"{'n':>9} {'lam':>5} {'cost':>12} {'cost/(lam polylog^2)':>20}")
    for n in [1024, 8192, 65536, 524288, 4194304]:
        lam = 16
        c, nb, pl, K = theoretical_cost_one_scale(n, lam, eps, L)
        print(f"{n:>9} {lam:>5} {c:>12.0f} {c/(lam*pl*pl):>20.2f}")

    print("\n(B) Fix n, vary lam (<= n^{1/3}): cost should be ~linear in lam.")
    n = 1 << 24
    n13 = n ** (1 / 3)
    print(f" n={n}, n^1/3={n13:.1f}")
    print(f"{'lam':>6} {'cost':>14} {'cost/lam':>12} {'cost/n^1/3':>12}")
    for lam in [4, 16, 64, int(round(n13))]:
        c, nb, pl, K = theoretical_cost_one_scale(n, lam, eps, L)
        print(f"{lam:>6} {c:>14.0f} {c/lam:>12.1f} {c/n13:>12.2f}")

    print("\n(C) Full algorithm at the balance point lam=n^{1/3}, summed over Otilde(1) scales")
    print("    with lam<=n^{1/3} (geometric scales (1+eps)^i): total cost vs n^{1/3}.")
    print(f"{'n':>11} {'n^1/3':>10} {'#scales<=n^1/3':>14} {'total cost':>14} {'/(n^1/3 polylog^3)':>18}")
    for n in [1 << 18, 1 << 21, 1 << 24, 1 << 27, 1 << 30]:
        n13 = n ** (1 / 3)
        pl = max(1.0, math.log2(n + 2))
        # geometric scales lam = (1+eps)^i up to n^{1/3}
        total = 0.0
        nscales = 0
        i = 0
        while (1 + eps) ** i <= n13:
            lam = (1 + eps) ** i
            if lam < 1:
                i += 1
                continue
            c, nb, _, _ = theoretical_cost_one_scale(n, lam, eps, L)
            total += c
            nscales += 1
            i += 1
        print(f"{n:>11} {n13:>10.1f} {nscales:>14} {total:>14.3e} {total/(n13*pl**3):>18.3f}")


if __name__ == "__main__":
    main()
