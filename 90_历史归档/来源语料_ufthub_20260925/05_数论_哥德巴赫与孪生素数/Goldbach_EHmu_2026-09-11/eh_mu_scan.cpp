// Reproducible finite EH_mu audit. This program does not prove Goldbach.
// Compile: g++ -O3 -std=c++17 eh_mu_scan.cpp -o eh_mu_scan
// Run: ./eh_mu_scan 1000000 3981 > scan.txt
// All moduli 1 <= q <= Q, all reduced residue classes, every integer 0 <= y < E.
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <vector>

struct Node {
    double lo_p, hi_p, lo_t, hi_t;
};

struct Tree {
    int base;
    std::vector<Node> nodes;
    explicit Tree(int q) {
        base = 1;
        while (base < q) base *= 2;
        const double inf = std::numeric_limits<double>::infinity();
        nodes.assign(2 * base, {inf, -inf, inf, -inf});
        for (int r = 0; r < q; ++r)
            if (std::gcd(r, q) == 1) nodes[base + r] = {0, 0, 0, 0};
        for (int i = base - 1; i; --i) pull(i);
    }
    void pull(int i) {
        const auto &a = nodes[2 * i], &b = nodes[2 * i + 1];
        nodes[i] = {std::min(a.lo_p, b.lo_p), std::max(a.hi_p, b.hi_p),
                    std::min(a.lo_t, b.lo_t), std::max(a.hi_t, b.hi_t)};
    }
    void add(int r, double w, double a) {
        int i = base + r;
        nodes[i].lo_p += w;
        nodes[i].hi_p += w;
        nodes[i].lo_t += a;
        nodes[i].hi_t += a;
        for (i /= 2; i; i /= 2) pull(i);
    }
};

int main(int argc, char **argv) {
    if (argc != 3) throw std::runtime_error("Expected E Q");
    int E = std::stoi(argv[1]), Q = std::stoi(argv[2]);
    if (E < 4 || E % 2 || Q < 1 || Q >= E)
        throw std::runtime_error("Require even E >= 4 and 1 <= Q < E");
    std::vector<int> lp(E), mu(E), primes;
    mu[1] = 1;
    for (int n = 2; n < E; ++n) {
        if (!lp[n]) { lp[n] = n; primes.push_back(n); mu[n] = -1; }
        for (int p : primes) {
            long long v = 1LL * p * n;
            if (v >= E || p > lp[n]) break;
            lp[v] = p;
            if (p == lp[n]) { mu[v] = 0; break; }
            mu[v] = -mu[n];
        }
    }
    std::vector<double> lam(E);
    for (int p : primes)
        for (long long n = p; n < E; n *= p) {
            lam[n] = std::log(static_cast<double>(p));
            if (n > (E - 1) / p) break;
        }
    std::vector<int> support;
    std::vector<double> w, a, prefix_p, prefix_t;
    long double total_p = 0, total_t = 0;
    for (int n = 2; n < E; ++n) if (lam[n] != 0) {
        support.push_back(n); w.push_back(lam[n]); a.push_back(lam[n] * mu[E - n]);
        total_p += w.back(); total_t += a.back();
        prefix_p.push_back(static_cast<double>(total_p));
        prefix_t.push_back(static_cast<double>(total_t));
    }
    std::cout << std::setprecision(17);
    std::cout << "# E " << E << " Q " << Q << " psi " << static_cast<double>(total_p)
              << " M " << static_cast<double>(total_t) << "\n";
    std::cout << "# q phi end_control_total end_control_y end_twist max_control_total "
                 "max_control_y max_twist wrong_control_all_r wrong_twist_all_r\n";
    for (int q = 1; q <= Q; ++q) {
        std::vector<char> reduced(q);
        int phi = 0;
        for (int r = 0; r < q; ++r) {
            reduced[r] = std::gcd(r, q) == 1; phi += reduced[r];
        }
        const double invphi = 1.0 / phi;
        Tree tree(q);
        std::vector<double> sum_p(q), sum_t(q);
        double max_p = 0, max_y = 0, max_t = 0;
        auto update_y = [&](int y) {
            const auto &v = tree.nodes[1];
            const double center = y * invphi;
            max_y = std::max({max_y, v.hi_p - center, center - v.lo_p});
        };
        for (size_t j = 0; j < support.size(); ++j) {
            const int n = support[j], r = n % q;
            // The classical y/phi center moves even between nonzero Lambda events.
            update_y(n - 1);
            sum_p[r] += w[j]; sum_t[r] += a[j];
            if (reduced[r]) tree.add(r, w[j], a[j]);
            const auto &v = tree.nodes[1];
            const double cp = prefix_p[j] * invphi, ct = prefix_t[j] * invphi;
            max_p = std::max({max_p, v.hi_p - cp, cp - v.lo_p});
            max_t = std::max({max_t, v.hi_t - ct, ct - v.lo_t});
            update_y(n);
        }
        update_y(E - 1);
        const auto &v = tree.nodes[1];
        const double cp = static_cast<double>(total_p) * invphi;
        const double ct = static_cast<double>(total_t) * invphi;
        const double cy = (E - 1) * invphi;
        double wrong_p = 0, wrong_t = 0;
        for (int r = 0; r < q; ++r) {
            wrong_p = std::max(wrong_p, std::abs(sum_p[r] - cp));
            wrong_t = std::max(wrong_t, std::abs(sum_t[r] - ct));
        }
        std::cout << q << ' ' << phi << ' '
                  << std::max(v.hi_p - cp, cp - v.lo_p) << ' '
                  << std::max(v.hi_p - cy, cy - v.lo_p) << ' '
                  << std::max(v.hi_t - ct, ct - v.lo_t) << ' '
                  << max_p << ' ' << max_y << ' ' << max_t << ' '
                  << wrong_p << ' ' << wrong_t << '\n';
    }
}
