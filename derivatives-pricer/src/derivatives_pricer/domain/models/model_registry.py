from derivatives_pricer.domain.models.pricing_model import PricingModel


class ModelRegistry:

    def __init__(self):
        self._models: dict[str, PricingModel] = {}

    def register(self, name: str, model: PricingModel) -> None:
        if not isinstance(model, PricingModel):
            raise TypeError(
                f"'{type(model).__name__}' must inherit from PricingModel."
            )
        self._models[name] = model

    def get(self, name: str) -> PricingModel:
        model = self._models.get(name)
        if model is None:
            available = list(self._models.keys())
            raise KeyError(
                f"Unknown model '{name}'. Available models: {available}"
            )
        return model

    @property
    def available_models(self) -> list[str]:
        return list(self._models.keys())