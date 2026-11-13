"""The sampling projection removes a gradient. The penalty sees it."""

from __future__ import annotations

import torch

from milady.train.constraints import divergence_penalty, project_solenoidal


def test_projection_removes_a_pure_gradient():
    k = torch.tensor([[0.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=torch.float64)
    coeff = k.to(torch.complex128)
    out = project_solenoidal(coeff, k)
    dot = (out * k).sum(-1).abs()
    assert torch.all(dot < 1e-12)
    assert float(divergence_penalty(out, k)) < 1e-20


def test_a_transverse_field_is_unchanged_and_costs_nothing():
    k = torch.tensor([[0.0, 0.0, 2.0]], dtype=torch.float64)
    transverse = torch.tensor([[[1.0, 0.0, 0.0]]], dtype=torch.complex128)
    out = project_solenoidal(transverse, k)
    assert torch.allclose(out, transverse)
    assert float(divergence_penalty(transverse, k)) == 0.0


def test_the_penalty_is_positive_on_a_gradient():
    k = torch.tensor([[1.0, 0.0, 0.0]], dtype=torch.float64)
    grad = torch.tensor([[[2.0, 0.0, 0.0]]], dtype=torch.complex128)
    assert float(divergence_penalty(grad, k)) > 0.0
