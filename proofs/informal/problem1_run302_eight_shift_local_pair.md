# Problem 1 run 302: eight-shift local pair

Problem 1 remains open. This continues run 301.

At phase t write a=alpha_t, c=c_t, d=d_t, v=x8(t), z=x7(t),
y=x6(t), w=x5(t), q=(y OR w), and

K = a+d+v+ad+cd+cv+cz+dz.

Run 301 proved Delta B_t = 1+d+v+dz+qK.

For the eight-shift put h=x3(t), p=p_t,
e=x7(t+8)+x7(t), f=x8(t+8)+x8(t), and
m=alpha_(t+8)+alpha_t.  The established transport laws are

a+=a+m, c+=c+h, d+=d+p, v+=v+f, z+=z+e, y+=y+1, w+=w.

Thus q+=(y+1 OR w)=q+1+w.  If K+ is K after this shift and L=K++K,
direct Boolean-ring simplification gives

L = m(1+d+p) + f(1+c+h)
  + p(1+a+c+e+h+z)
  + e(c+d+h) + h(d+v+z).

Therefore, for S_t = Delta B_t + Delta B_(t+8),

S_t = p+f+de+pz+pe + qL + (1+w)K+,

equivalently

S_t = p+f+de+pz+pe + (1+w)K + q+L.

The full run-300 target is only D_(t+1)+D_t = S_t+S_(t+4).

## Exact finite certificate for the remaining four-shift comparison

I evaluated the exact triangular Rule-30 recurrence on all 128 restricted
states (p,x3,x4,x5,x6,x7,x8), retaining the original run-262 global scalar a.
In that variable order the ANF masks are

S_0:
2,4,9,11,12,13,25,26,29,30,37,39,41,43,49,51,53,55,57,59,65,67,69,71,73,74

S_4:
0,2,4,8,11,12,13,25,26,29,30,37,39,41,43,49,51,53,55,57,59,65,67,69,71,73,74

They have the same 25-monomial high-coordinate core. Their symmetric
difference is exactly masks 0,8,9, hence

S_4+S_0 = 1+x5+p*x5 = 1+x5(1+p).

This is a smaller certificate than runs 299-300: the remaining four-shift
comparison is equality of one common 25-monomial core plus three boundary
masks.

I also exhausted all 254 nonconstant affine linear Boolean functions on the
seven variables as possible factors of that common core. None divides it.
So trying to factor the common core by a linear selector is a dead end.
The useful analytic target is instead to transport the compact S formula by
four steps and cancel the common core as a whole, especially the m and f
cocycle terms.
