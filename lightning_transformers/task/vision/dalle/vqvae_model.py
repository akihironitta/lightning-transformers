from typing import Any

import hydra
import torch

from lightning_transformers.core import TaskTransformer
from lightning_transformers.core.hydra_model import HydraTaskTransformer


class VQVAE(TaskTransformer):
    def __init__(
        self,
        backbone,
        optimizer: Any,
        scheduler: Any,
        **config_data_args,
    ):
        super().__init__(optimizer, scheduler)
        self.save_hyperparameters()
        self.model = hydra.utils.instantiate(backbone, **config_data_args)

    def training_step(self, batch: Any, batch_idx: int) -> torch.Tensor:
        images, labels = batch
        loss = self.model(images, return_recon_loss=True)
        return loss

    def test_step(self, batch: Any, batch_idx: int) -> torch.Tensor:
        return self.common_step(batch, "test")

    def validation_step(self, batch: Any, batch_idx: int) -> torch.Tensor:
        return self.common_step(batch, "validation")

    def common_step(self, batch: Any, prefix) -> torch.Tensor:
        images, labels = batch
        loss = self.model(images, return_recon_loss=True)
        self.log(f"{prefix}_loss", loss, prog_bar=True, on_epoch=True, on_step=False)
        return loss
