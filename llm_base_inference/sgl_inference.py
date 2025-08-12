import os
import time
import argparse
import sglang as sgl


def parse_args():
    parser = argparse.ArgumentParser(description="SGL Language Demo")
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen3-4B-Base", help="Model name or path")
    parser.add_argument("--num_gpus", type=int, default=1, help="Number of GPUs to use for data parallelism")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for sampling")
    parser.add_argument("--top_p", type=float, default=0.95, help="Top-p for sampling")
    parser.add_argument("--max_new_tokens", type=int, default=128, help="Maximum number of tokens to generate")
    return parser.parse_args()


def generate(llm, prompts, sampling_params):
    outputs = llm.generate(prompts, sampling_params)
    responses = [output['text'] for output in outputs]
    return responses


def get_test_prompts():
    return [
        {
            "prompt": "Complete this sentence: The capital of France is",
            "expected": "Paris"
        },
        {
            "prompt": "What is 2+2?",
            "expected": "4"
        },
        {
            "prompt": "Translate 'hello' to Spanish:",
            "expected": "hola"
        },
        {
            "prompt": "Name a primary color:",
            "expected_options": ["red", "blue", "yellow"]
        }
    ]


def evaluate_response(response, expected):
    """Simple evaluation function to check if response contains expected answer."""
    if isinstance(expected, list):
        return any(exp.lower() in response.lower() for exp in expected)
    return expected.lower() in response.lower()


if __name__ == "__main__":
    args = parse_args()
   
    llm = sgl.Engine(
        model_path=args.model_name,
        dp_size=args.num_gpus,
        tp_size=1,
        device="cuda",
        context_length=1000
    )
    
    test_data = get_test_prompts()
    prompts = [item["prompt"] for item in test_data]
    

    sampling_params = {
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_new_tokens": args.max_new_tokens
    }
    
    # Generate responses and measure time
    t0 = time.time()
    responses = generate(llm, prompts, sampling_params)
    t1 = time.time()
    
    # Evaluate responses
    total_score = 0
    for i, (response, test_item) in enumerate(zip(responses, test_data)):
        expected = test_item.get("expected_options", test_item.get("expected"))
        is_correct = evaluate_response(response, expected)
        
        print(f"Prompt {i+1}: {test_item['prompt']}")
        print(f"Response: {response}")
        print(f"Expected: {expected}")
        print(f"Correct: {is_correct}")
        print("-" * 50)
        
        if is_correct:
            total_score += 1
    
    print(f"Accuracy: {total_score}/{len(prompts)} = {total_score / len(prompts):.2f}")
    print(f"Time taken: {t1 - t0:.4f} seconds")

    llm.shutdown()
