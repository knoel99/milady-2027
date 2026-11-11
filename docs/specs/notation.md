# Common notation

| Object | Notation | Remark |
|---|---|---|
| Domain, boundary | $\Omega \subset \mathbb{R}^d$, $\partial\Omega$, outward normal $\mathbf{n}$ | $d = 2$ or $3$ |
| Velocity, magnetic field | $\mathbf{u}(\mathbf{x}, t)$, $\mathbf{B}(\mathbf{x}, t)$ | $\mathbf{B}$ in Alfvén units ($\mathbf{B}/\sqrt{\mu_0 \rho}$) |
| Vorticity, current density | $\boldsymbol{\omega} = \nabla\times\mathbf{u}$, $\mathbf{j} = \nabla\times\mathbf{B}$ | in 2D: scalars $\omega$, $j$ |
| Potentials | stream function $\psi$ ($\mathbf{u} = \nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$), magnetic potential $a$ ($\mathbf{B} = \nabla^\perp a$); vector potential $\mathbf{A}$ ($\mathbf{B} = \nabla\times\mathbf{A}$) in 3D | |
| Viscosity, magnetic diffusivity | $\nu$, $\eta = 1/(\mu_0\sigma)$ | |
| Kolmogorov scales (P2) | $\ell_K = (\nu^3/\varepsilon)^{1/4}$, $\tau_K$, $u_K$ | never $\eta$, which is the magnetic diffusivity |
| Dimensionless numbers | $Re = UL/\nu$, $Rm = UL/\eta$, $Pm = \nu/\eta = Rm/Re$ | |
| Spatial average | $\langle f \rangle = \frac{1}{|\Omega|}\int_\Omega f\,\mathrm{d}\mathbf{x}$ | |
| Energy | $E = \tfrac12\langle |\mathbf{u}|^2 + |\mathbf{B}|^2\rangle$ | |
| Helicities | kinetic $H_K = \langle \mathbf{u}\cdot\boldsymbol\omega\rangle$, magnetic $H_M = \langle \mathbf{A}\cdot\mathbf{B}\rangle$, cross $H_C = \langle \mathbf{u}\cdot\mathbf{B}\rangle$ | |
| Control parameters | $\boldsymbol{\lambda}$ (e.g. $Re$, $Rm$, $Pm$, $\Gamma$) | model conditioning |
| Discrete state | $\mathbf{x} \in \mathbb{R}^D$ | discretized field |
| Data law, generated law | $\mu_{\boldsymbol\lambda}$, $q_{\boldsymbol\lambda}$ (or $q_\theta(\cdot\mid\boldsymbol\lambda)$) | |
| Noise, flow time | $\mathbf{x}_0 \sim \mathcal{N}(0, I)$, $t \in [0, 1]$, $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$ | flow matching convention ($t=1$: data) |
| Flow velocity field | $v_\theta(\mathbf{x}, t, \boldsymbol\lambda)$ | not to be confused with the physical velocity $\mathbf{u}$ |
| Physical dynamics | $\dot{\mathbf{x}} = F_{\boldsymbol\lambda}(\mathbf{x})$ (+ noise $\sigma\,\mathrm{d}W$) | generator $\mathcal{L}_{\boldsymbol\lambda}\varphi = F\cdot\nabla\varphi + \tfrac{\sigma^2}{2}\Delta\varphi$ |
| Divergences between laws | $\mathrm{KL}(p\,\|\,q)$, $W_p$, energy distance $\mathcal{E}$ | |
