#!/usr/bin/env python3

import os
from dotenv import load_dotenv
load_dotenv()

from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness, context_precision, context_recall
from datasets import Dataset

def debug_ragas():
    print("Debugging RAGAS Evaluation")
    print("=" * 40)
    
    # Test with simple data
    contexts = ["Coercive control is a criminal offence in Ireland under the Domestic Violence Act 2018."]
    
    ragas_data = {
        "question": ["What is coercive control under Irish law?"],
        "answer": ["Coercive control is a criminal offence in Ireland since 2019 under the Domestic Violence Act 2018."], 
        "contexts": [contexts],
        "ground_truth": ["Coercive control is criminalized under Irish law."]
    }
    
    print("Creating dataset...")
    dataset = Dataset.from_dict(ragas_data)
    print(f"Dataset created: {dataset}")
    print(f"Dataset columns: {dataset.column_names}")
    print(f"Dataset features: {dataset.features}")
    
    try:
        print("\nRunning RAGAS evaluation...")
        evaluation_result = evaluate(
            dataset=dataset,
            metrics=[
                answer_relevancy,
                faithfulness,
                context_precision,
                context_recall
            ]
        )
        
        print(f"RAGAS completed successfully!")
        print(f"Result type: {type(evaluation_result)}")
        print(f"Result keys: {evaluation_result.keys() if hasattr(evaluation_result, 'keys') else 'No keys method'}")
        print(f"Result: {evaluation_result}")
        
        # Try to extract scores
        print("\nExtracting scores...")
        for metric_name in ['answer_relevancy', 'faithfulness', 'context_precision', 'context_recall']:
            try:
                score = evaluation_result[metric_name]
                print(f"{metric_name}: {score} (type: {type(score)})")
                
                # Try different extraction methods
                try:
                    if hasattr(score, 'item'):
                        print(f"  .item(): {score.item()}")
                    if hasattr(score, '__float__'):
                        print(f"  float(): {float(score)}")
                    print(f"  final value: {float(score)}")
                except Exception as ex:
                    print(f"  extraction error: {ex}")
            except KeyError:
                print(f"{metric_name}: NOT FOUND")
            except Exception as ex:
                print(f"{metric_name}: ACCESS ERROR - {ex}")
        
    except Exception as e:
        print(f"RAGAS failed with exception:")
        print(f"Exception type: {type(e)}")
        print(f"Exception str: '{str(e)}'")
        print(f"Exception repr: {repr(e)}")
        print(f"Exception args: {e.args}")
        
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_ragas()