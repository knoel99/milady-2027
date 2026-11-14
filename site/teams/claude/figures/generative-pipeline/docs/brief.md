# Brief: generative pipeline
Mode describe, depth full, route flat, width 183 mm. Takeaway: the model generates the Fourier modes of the vector potentials, so every sample is divergence-free by construction.
Key ideas: snapshots (u, B) on the 16^3 grid -> 665 complex Fourier modes (|m_i| <= 5) -> vector potentials in the Craya-Herring basis (latent of 5320 reals) -> conditional flow matching conditioned on log eta -> sampling by integrating the flow -> decoding B = curl A.
Must not imply: that samples match the reference law; any result number; quadratic budgets of the solver (not in FACTS.md). Source: FACTS.md only.
