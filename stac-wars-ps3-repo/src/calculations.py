"""Radius, orbit and habitability numbers for STAC-1/2/3 (PS3)."""
import math

R_SUN, R_EARTH, AU, YEAR = 696_000, 6_371, 149.6e6, 365.25

# period (d) and depth are read from the light curves in ../data
STARS = {
    "STAC-1": dict(M=1.0, R=1.0, L=1.0, T=5800, depth=0.0030,  P=4.25),
    "STAC-2": dict(M=0.8, R=0.8, L=0.4, T=5000, depth=0.0010,  P=80.0),
    "STAC-3": dict(M=0.5, R=0.5, L=0.08, T=3800, depth=0.00088, P=38.0),
}

for name, s in STARS.items():
    rs = s["R"] * R_SUN
    rp = rs * math.sqrt(s["depth"])            # depth = (Rp/Rs)^2
    p_yr = s["P"] / YEAR
    a = (s["M"] * p_yr**2) ** (1 / 3)          # P^2 = a^3 / M
    d_hz = math.sqrt(s["L"])
    flux = s["L"] / a**2
    t_eq = s["T"] * math.sqrt(rs / (2 * a * AU))  # zero albedo
    print(f"{name}: Rp={rp:,.0f} km ({rp/R_EARTH:.2f} Re)  a={a:.4f} AU "
          f"({a*AU:.3e} km)  a/dHZ={a/d_hz:.2f}  S={flux:.1f} Searth  Teq={t_eq:.0f} K")
