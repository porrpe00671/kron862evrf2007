import math
from pyproj import Transformer


class Converter:

    def __init__(self):
        self.K0 = 0.999923
        self.E = 0.00669438

        self.E2 = self.E * self.E
        self.E3 = self.E2 * self.E
        self.E_P2 = self.E / (1 - self.E)

        self.SQRT_E = math.sqrt(1 - self.E)
        self._E = (1 - self.SQRT_E) / (1 + self.SQRT_E)
        self._E2 = self._E * self._E
        self._E3 = self._E2 * self._E
        self._E4 = self._E3 * self._E
        self._E5 = self._E4 * self._E

        self.M1 = (1 - self.E / 4 - 3 * self.E2 / 64 - 5 * self.E3 / 256)
        self.M2 = (3 * self.E / 8 + 3 * self.E2 / 32 + 45 * self.E3 / 1024)
        self.M3 = (15 * self.E2 / 256 + 45 * self.E3 / 1024)
        self.M4 = (35 * self.E3 / 3072)

        self.P2 = (3 / 2 * self._E - 27 / 32 * self._E3 + 269 / 512 * self._E5)
        self.P3 = (21 / 16 * self._E2 - 55 / 32 * self._E4)
        self.P4 = (151 / 96 * self._E3 - 417 / 128 * self._E5)
        self.P5 = (1097 / 512 * self._E4)

        self.R = 6378137

        self.k0 = self.K0
        self._a = self.R
        self._b = 6356752.31424518

        self.e = math.sqrt(self._a * self._a - self._b * self._b) / self._a
        self.e_ = math.sqrt(self._a * self._a - self._b * self._b) / self._b
        self.e_2 = self.e_ * self.e_
        self.c = self._a * self._a / self._b

    def Method1(self, X, Y):
        y = Y
        x = X - 7500000

        m = y / self.K0
        mu = m / (self.R * self.M1)

        p_rad = (mu +
                 self.P2 * math.sin(2 * mu) +
                 self.P3 * math.sin(4 * mu) +
                 self.P4 * math.sin(6 * mu) +
                 self.P5 * math.sin(8 * mu))

        p_sin = math.sin(p_rad)
        p_sin2 = p_sin * p_sin

        p_cos = math.cos(p_rad)

        p_tan = p_sin / p_cos
        p_tan2 = p_tan * p_tan
        p_tan4 = p_tan2 * p_tan2

        ep_sin = 1 - self.E * p_sin2
        ep_sin_sqrt = math.sqrt(1 - self.E * p_sin2)

        n = self.R / ep_sin_sqrt
        r = (1 - self.E) / ep_sin

        c = self.E_P2 * p_cos**2
        c2 = c * c

        d = x / (n * self.K0)
        d2 = d * d
        d3 = d2 * d
        d4 = d3 * d
        d5 = d4 * d
        d6 = d5 * d

        latitude = (p_rad - (p_tan / r) *
                    (d2 / 2 -
                    d4 / 24 * (5 + 3 * p_tan2 + 10 * c - 4 * c2 - 9 * self.E_P2)) +
                    d6 / 720 * (61 + 90 * p_tan2 + 298 * c + 45 * p_tan4 - 252 * self.E_P2 - 3 * c2))

        longitude = (d -
                     d3 / 6 * (1 + 2 * p_tan2 + c) +
                     d5 / 120 * (5 - 2 * c + 28 * p_tan2 - 3 * c2 + 8 * self.E_P2 + 24 * p_tan4)) / p_cos

        return (math.degrees(latitude), math.degrees(longitude) + 21)

    def Method2(self, X, Y):
        y = Y
        x = X - 7500000

        fi = y / (6366197.724 * self.k0)
        ni = self.c / ((1 + self.e_2 * math.cos(fi)**2)**0.5)*self.k0

        a = (x - 0) / ni
        A1 = math.sin(2 * fi)
        A2 = A1 * math.cos(fi) ** 2
        J2 = fi + A1 / 2
        J4 = (3 * J2 + A2) / 4
        J6 = (5 * J4 + A2 * math.cos(fi) ** 2) / 3
        Alfa = 0.75 * self.e_2
        Beta = (5 / 3) * Alfa ** 2
        Gamma = (35 / 27) * Alfa ** 3
        Bfi = self.k0 * self.c * (fi - Alfa * J2 + Beta * J4 - Gamma * J6)
        b = (y - Bfi) / ni
        Zeta = self.e_2 * a ** 2 / 2 * math.cos(fi) ** 2
        Xi = a * (1 - Zeta / 3)
        Eta = b * (1 - Zeta) + fi
        SenhXi = (math.exp(Xi) - math.exp(-Xi)) / 2
        Dlam = math.atan(SenhXi / math.cos(Eta))
        Tau = math.atan(math.cos(Dlam) * math.tan(Eta))

        long = Dlam / math.pi * 180 + 21
        _lat = fi+(1 + self.e_2*(math.cos(fi)) ** 2-(3/2) * self.e_2 *
                   math.sin(fi)*math.cos(fi)*(Tau-fi))*(Tau-fi)
        lat = _lat / math.pi * 180

        return (lat, long)

    def Method3(self, x, y):
        transformer = Transformer.from_crs("EPSG:2178 ", "EPSG:5621")
        return transformer.transform(y, x)
