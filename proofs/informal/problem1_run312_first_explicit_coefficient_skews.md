# Problem 1 run 312: first explicit coefficient skews

Problem 1 remains open. Continue from run 311. All sums below are Boolean.

Run 302 contains the two coefficients

    A_t = 1+d_t+p_t
    B_t = 1+c_t+x_3(t)

multiplying m and f in L.

Run 304 gives

    d_(t+4)+d_t = j_t+j_(t+1)
    c_(t+4)+c_t = j_t.

Run 268 gives x_3(t+4)=x_3(t). The run-305 consistency identity p_t=x_3(t)+x_3(t+1) therefore gives p_(t+4)=p_t.

Hence

    A_(t+4)+A_t = j_t+j_(t+1)
    B_(t+4)+B_t = j_t.

So these two coefficient skews do not vanish, but they close entirely in the already controlled j sector. No coordinate 7 or 8 expansion is needed.

Combining with run 311's product rule shows that a bare A-weighted u term can leave only (j_t+j_(t+1))u_t as its high residual, while a B-weighted u term can leave only j_t u_t; all other pieces descend to coordinate 6.

Caveat: in S_t, L is multiplied by qplus=q+1+x_5. Thus the full coefficients require the four-step skew of qplus as well. The next target is to compute that low-coordinate skew from q=x_6 OR x_5 and the known four-step x_6/x_5 cocycles, then reduce the resulting mixed j*u terms.

Blocker: coefficient transport has now been reduced from arbitrary high-coordinate functions to the low qplus skew and mixed j*u products.
