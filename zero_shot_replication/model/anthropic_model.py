from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic

from zero_shot_replication.model.base import (
    LargeLanguageModel,
    ModelName,
    PromptMode,
    Quantization,
)


class AnthropicModel(LargeLanguageModel):
    """A concrete class for creating Anthropic models."""

    def __init__(
        self,
        model_name: ModelName,
        quantization: Quantization,
        temperature: float,
        stream: bool,
        max_tokens_to_sample: int,
    ) -> None:
        if stream:
            raise ValueError(
                "Stream is not supported for Anthropic in this framework."
            )

        super().__init__(
            model_name,
            quantization,
            temperature,
            stream,
            prompt_mode=PromptMode.HUMAN_FEEDBACK,
        )
        self.anthropic = Anthropic()
        self.max_tokens_to_sample = max_tokens_to_sample

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided messages."""

        formatted_prompt = f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}"

        completion = self.anthropic.completions.create(
            model=self.model_name.value,
            max_tokens_to_sample=self.max_tokens_to_sample,
            stream=self.stream,
            prompt=formatted_prompt,
            temperature=self.temperature,
        )  # type: ignore
        return completion.completion
