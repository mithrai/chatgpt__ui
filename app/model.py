from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

generator = None

def generate_response(prompt: str) -> str:
    global generator

    # Load model lazily and only once
    if generator is None:
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model = AutoModelForCausalLM.from_pretrained("gpt2")
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    # Clear instruction prompt for GPT-2
    full_prompt = f"Q: {prompt}\nA:"

    # Generate response with controlled decoding
    output = generator(
        full_prompt,
        max_new_tokens=100,
        do_sample=False,     # Deterministic output
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1
    )[0]["generated_text"]

    # Extract only the answer part
    response = output.split("A:")[-1].strip()

    return response
