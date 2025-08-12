import os
import time
import logging
from omegaconfig import OmegaConf
import pandas as pd
import polars as pl
import torch
import transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor
from vllm.transformers_utils.tokenizer import get_tokenizer
import vllm
import ray
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


PROMPT = """Classify the following text into one of these categories: positive, negative, or neutral.
Respond with only the category name.

Text: {text}

Category:"""


def build_df_data() -> pd.DataFrame:
    """Create sample data for demonstration"""
    sample_texts = [
        "I love this product! It's amazing and works perfectly.",
        "This is terrible. Worst purchase ever made.",
        "The weather is okay today, nothing special.",
        "Fantastic service and great customer support!",
        "It's just an average product, nothing more.",
        "I hate waiting in long lines at the store.",
        "The book was quite interesting and well-written.",
        "Meh, could be better but could be worse too.",
        "Outstanding performance, exceeded my expectations!",
        "This software is buggy and crashes frequently."
    ]
    
    df = pd.DataFrame({
        'text': sample_texts,
        'id': range(len(sample_texts))
    })
    
    logger.info(f"Created sample dataset with {len(df)} rows")
    return df


class PromptPreparer:
    """Prepares prompts for text classification"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.tokenizer = None
        
    def __call__(self, batch: Dict[str, List]) -> Dict[str, List]:
        """Process a batch of rows to prepare prompts"""
        if self.tokenizer is None:
            try:
                self.tokenizer = get_tokenizer(self.model_name)
                logger.info(f"Loaded tokenizer for {self.model_name}")
            except Exception as e:
                logger.warning(f"Could not load tokenizer: {e}. Using simple prompt formatting.")
                self.tokenizer = None
        
        # Process each text in the batch
        prompts = []
        for text in batch['text']:
            if self.tokenizer is not None:
                messages = [
                    {"role": "user", "content": PROMPT.format(text=text)}
                ]
                try:
                    prompt = self.tokenizer.apply_chat_template(
                        messages, tokenize=False, add_generation_prompt=True
                    )
                except:
                    # Fallback if chat template not supported
                    prompt = PROMPT.format(text=text)
            else:
                prompt = PROMPT.format(text=text)
            
            prompts.append(prompt)
        
        batch['prompt'] = prompts
        return batch
    

def generate_batch_response(batch: Dict[str, List]) -> Dict[str, List]:
    """Generate responses for a batch of prompts using OpenAI API"""
    
    # Configuration - in production, use environment variables
    api_base_url = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
    api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
    model_name = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
    max_retries = int(os.getenv('MAX_RETRIES', '3'))
    
    # Initialize OpenAI client
    client = OpenAI(
        base_url=api_base_url,
        api_key=api_key
    )
    
    responses = []
    
    for i, prompt in enumerate(batch['prompt']):
        response_text = "error"
        
        for attempt in range(max_retries):
            try:
                # Create chat completion
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=50,  # Reduced for classification task
                    timeout=30
                )
                
                response_text = response.choices[0].message.content.strip()
                logger.debug(f"Successfully processed item {i}")
                break
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for item {i}: {str(e)}")
                if attempt == max_retries - 1:
                    response_text = f"Error after {max_retries} attempts: {str(e)}"
                else:
                    time.sleep(1)  # Brief delay before retry
        
        responses.append(response_text)
    
    batch['response'] = responses
    return batch


def main():
    """Main execution function"""
    start_time = time.time()
    
    # Initialize Ray
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)
        logger.info("Ray initialized")
    
    try:
        # Build sample data
        df = build_df_data()
        
        # Convert to Ray dataset
        ds = ray.data.from_pandas(df)
        logger.info("Created Ray dataset")
        
        # Prepare prompts
        prompt_preparer = PromptPreparer(model_name="microsoft/DialoGPT-medium")
        ds = ds.map_batches(prompt_preparer, batch_size=5)
        logger.info("Prompts prepared")

        logger.info("Using OpenAI API for classification")           
        ds = ds.map_batches(generate_batch_response, batch_size=2)
        
        # Collect results
        logger.info("Collecting results...")
        results = ds.to_pandas()
        
        # Calculate processing time
        end_time = time.time()
        processing_time = end_time - start_time
        
        logger.info(f"Processing completed in {processing_time:.2f} seconds")
        logger.info(f"Processed {len(results)} items")        
       
        # Save results
        output_file = "classification_results.csv"
        results.to_csv(output_file, index=False)
        logger.info(f"Results saved to {output_file}")        
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise
    
    finally:
        if ray.is_initialized():
            ray.shutdown()
            logger.info("Ray shutdown complete")


if __name__ == "__main__":
    os.environ.setdefault('MAX_RETRIES', '3')
    main()
