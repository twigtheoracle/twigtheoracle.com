/*
Fraction.js v4.0.4 09/09/2015
http://www.xarg.org/2014/03/rational-numbers-in-javascript/

Copyright (c) 2015, Robert Eisele (robert@xarg.org)
Dual licensed under the MIT or GPL Version 2 licenses.
*/
(function (w) {
    function m(a, b) {
        if (!a) return b;
        if (!b) return a;
        for (;;) {
            a %= b;
            if (!a) return b;
            b %= a;
            if (!b) return a
        }
    }

    function l(a, b) {
        var c = 0,
            e = 1,
            g = 1,
            k = 0,
            l = 0,
            m = 0,
            t = 1,
            q = 1,
            f = 0,
            h = 1,
            r = 1,
            n = 1;
        if (void 0 !== a && null !== a)
            if (void 0 !== b) c = a, e = b, g = c * e;
            else switch (typeof a) {
                case "object":
                    "d" in a && "n" in a ? (c = a.n, e = a.d, "s" in a && (c *= a.s)) : 0 in a ? (c = a[0], 1 in a && (e = a[1])) : u();
                    g = c * e;
                    break;
                case "number":
                    0 > a && (g = a, a = -a);
                    if (0 === a % 1) c = a;
                    else if (0 < a) {
                        1 <= a && (q = Math.pow(10, Math.floor(1 + Math.log(a) / Math.LN10)), a /= q);
                        for (; 1E7 >= h && 1E7 >=
                            n;)
                            if (c = (f + r) / (h + n), a === c) {
                                1E7 >= h + n ? (c = f + r, e = h + n) : n > h ? (c = r, e = n) : (c = f, e = h);
                                break
                            } else a > c ? (f += r, h += n) : (r += f, n += h), 1E7 < h ? (c = r, e = n) : (c = f, e = h);
                        c *= q
                    } else if (isNaN(a) || isNaN(b)) e = c = NaN;
                    break;
                case "string":
                    h = a.match(/\d+|./g);
                    null === h && u();
                    "-" === h[f] ? (g = -1, f++) : "+" === h[f] && f++;
                    if (h.length === f + 1) l = p(h[f++], g);
                    else if ("." === h[f + 1] || "." === h[f]) {
                        "." !== h[f] && (k = p(h[f++], g));
                        f++;
                        if (f + 1 === h.length || "(" === h[f + 1] && ")" === h[f + 3] || "'" === h[f + 1] && "'" === h[f + 3]) l = p(h[f], g), t = Math.pow(10, h[f].length), f++;
                        if ("(" === h[f] &&
                            ")" === h[f + 2] || "'" === h[f] && "'" === h[f + 2]) m = p(h[f + 1], g), q = Math.pow(10, h[f + 1].length) - 1, f += 3
                    } else "/" === h[f + 1] || ":" === h[f + 1] ? (l = p(h[f], g), t = p(h[f + 2], 1), f += 3) : "/" === h[f + 3] && " " === h[f + 1] && (k = p(h[f], g), l = p(h[f + 2], g), t = p(h[f + 4], 1), f += 5);
                    if (h.length <= f) {
                        e = t * q;
                        g = c = m + e * k + q * l;
                        break
                    }
                default:
                    u()
            }
        if (0 === e) throw new x;
        d.s = 0 > g ? -1 : 1;
        d.n = Math.abs(c);
        d.d = Math.abs(e)
    }

    function v(a) {
        function b() {}

        function c() {
            var b = Error.apply(this, arguments);
            b.name = this.name = a;
            this.stack = b.stack;
            this.message = b.message
        }
        b.prototype = Error.prototype;
        c.prototype = new b;
        return c
    }

    function p(a, b) {
        isNaN(a = parseInt(a, 10)) && u();
        return a * b
    }

    function u() {
        throw new y;
    }

    function k(a, b) {
        if (!(this instanceof k)) return new k(a, b);
        l(a, b);
        a = k.REDUCE ? m(d.d, d.n) : 1;
        this.s = d.s;
        this.n = d.n / a;
        this.d = d.d / a
    }
    var d = {
            s: 1,
            n: 0,
            d: 1
        },
        x = k.DivisionByZero = v("DivisionByZero"),
        y = k.InvalidParameter = v("InvalidParameter");
    k.REDUCE = 1;
    k.prototype = {
        s: 1,
        n: 0,
        d: 1,
        abs: function () {
            return new k(this.n, this.d)
        },
        neg: function () {
            return new k(-this.s * this.n, this.d)
        },
        add: function (a, b) {
            l(a, b);
            return new k(this.s *
                this.n * d.d + d.s * this.d * d.n, this.d * d.d)
        },
        sub: function (a, b) {
            l(a, b);
            return new k(this.s * this.n * d.d - d.s * this.d * d.n, this.d * d.d)
        },
        mul: function (a, b) {
            l(a, b);
            return new k(this.s * d.s * this.n * d.n, this.d * d.d)
        },
        div: function (a, b) {
            l(a, b);
            return new k(this.s * d.s * this.n * d.d, this.d * d.n)
        },
        clone: function () {
            return new k(this)
        },
        mod: function (a, b) {
            if (isNaN(this.n) || isNaN(this.d)) return new k(NaN);
            if (void 0 === a) return new k(this.s * this.n % this.d, 1);
            l(a, b);
            0 === d.n && 0 === this.d && k(0, 0);
            return new k(this.s * d.d * this.n % (d.n * this.d),
                d.d * this.d)
        },
        gcd: function (a, b) {
            l(a, b);
            return new k(m(d.n, this.n) * m(d.d, this.d), d.d * this.d)
        },
        lcm: function (a, b) {
            l(a, b);
            return 0 === d.n && 0 === this.n ? new k : new k(d.n * this.n, m(d.n, this.n) * m(d.d, this.d))
        },
        ceil: function (a) {
            a = Math.pow(10, a || 0);
            return isNaN(this.n) || isNaN(this.d) ? new k(NaN) : new k(Math.ceil(a * this.s * this.n / this.d), a)
        },
        floor: function (a) {
            a = Math.pow(10, a || 0);
            return isNaN(this.n) || isNaN(this.d) ? new k(NaN) : new k(Math.floor(a * this.s * this.n / this.d), a)
        },
        round: function (a) {
            a = Math.pow(10, a || 0);
            return isNaN(this.n) ||
                isNaN(this.d) ? new k(NaN) : new k(Math.round(a * this.s * this.n / this.d), a)
        },
        inverse: function () {
            return new k(this.s * this.d, this.n)
        },
        pow: function (a) {
            return 0 > a ? new k(Math.pow(this.s * this.d, -a), Math.pow(this.n, -a)) : new k(Math.pow(this.s * this.n, a), Math.pow(this.d, a))
        },
        equals: function (a, b) {
            l(a, b);
            return this.s * this.n * d.d === d.s * d.n * this.d
        },
        compare: function (a, b) {
            l(a, b);
            var c = this.s * this.n * d.d - d.s * d.n * this.d;
            return (0 < c) - (0 > c)
        },
        divisible: function (a, b) {
            l(a, b);
            return !(!(d.n * this.d) || this.n * d.d % (d.n * this.d))
        },
        valueOf: function () {
            return this.s *
                this.n / this.d
        },
        toFraction: function (a) {
            var b, c = "",
                e = this.n,
                g = this.d;
            0 > this.s && (c += "-");
            1 === g ? c += e : (a && 0 < (b = Math.floor(e / g)) && (c = c + b + " ", e %= g), c = c + e + "/", c += g);
            return c
        },
        toLatex: function (a) {
            var b, c = "",
                e = this.n,
                g = this.d;
            0 > this.s && (c += "-");
            1 === g ? c += e : (a && 0 < (b = Math.floor(e / g)) && (c += b, e %= g), c = c + "\\frac{" + e + "}{" + g, c += "}");
            return c
        },
        toContinued: function () {
            var a = this.n,
                b = this.d,
                c = [];
            do {
                c.push(Math.floor(a / b));
                var e = a % b;
                a = b;
                b = e
            } while (1 !== a);
            return c
        },
        toString: function () {
            var a = this.n,
                b = this.d;
            if (isNaN(a) || isNaN(b)) return "NaN";
            if (!k.REDUCE) {
                var c = m(a, b);
                a /= c;
                b /= c
            }
            a: {
                for (c = b; 0 === c % 2; c /= 2);
                for (; 0 === c % 5; c /= 5);
                if (1 === c) c = 0;
                else {
                    for (var e = 10 % c, g = 1; 1 !== e; g++)
                        if (e = 10 * e % c, 2E3 < g) {
                            c = 0;
                            break a
                        }
                    c = g
                }
            }
            a: {
                e = 1;g = 10;
                for (var d = c, l = 1; 0 < d; g = g * g % b, d >>= 1) d & 1 && (l = l * g % b);g = l;
                for (d = 0; 300 > d; d++) {
                    if (e === g) {
                        g = d;
                        break a
                    }
                    e = 10 * e % b;
                    g = 10 * g % b
                }
                g = 0
            }
            e = -1 === this.s ? "-" : "";
            e += a / b | 0;
            (a = a % b * 10) && (e += ".");
            if (c) {
                for (; g--;) e += a / b | 0, a %= b, a *= 10;
                e += "(";
                for (g = c; g--;) e += a / b | 0, a %= b, a *= 10;
                e += ")"
            } else
                for (g = 15; a && g--;) e += a / b | 0, a %= b, a *= 10;
            return e
        }
    };
    "function" === typeof define &&
        define.amd ? define([], function () {
            return k
        }) : "object" === typeof exports ? module.exports = k : w.Fraction = k
})(this);
