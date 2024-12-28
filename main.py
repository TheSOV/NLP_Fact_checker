import os
from dotenv import load_dotenv
import time
import re

from flows.fact_checker_flow import FactCheckerFlow
from flows.get_summarized_source_flow import GetSummarizedSourceFlow

def sanitize_filename(filename):
    """Create a safe filename from the input string."""
    # Replace invalid characters with underscores
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove any other non-ASCII characters
    safe_name = ''.join(char for char in safe_name if ord(char) < 128)
    # Add timestamp to make it unique
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    microseconds = str(time.time_ns() // 1000 % 1000000).zfill(6)
    return f"{safe_name}_{timestamp}_{microseconds}.txt"

# The proteolytic activity of pepsin is reduced by 50 percent through addition of bisabolol
statements = [
    "América fue descubierta por el físico alemán Otto Hahn en 1919",
    # "La sal sube la presión arterial",
    # "La tierra es plana",
    # "Einstein fue un Químico Alemán, invertor de la ley de la gravedad",
    # "Newton fue el creador de la teoria de la relatividad",
    # "MArie Curie fue una Química Rusa que descubrió el radioactividad",	
    # "Bisabol increases proteolytic activity of pepsin",
    # "Bisabol decreases proteolytic activity of pepsin",
    # "Bisabol has no effect on the proteolytic activity of pepsin",
    # "Cinco hidrolasas de ésteres distintas han sido caracterizadas en la epidermis del conejillo de Indias",
    # "Las Cinco hidrolasas de ésteres distintas han sido caracterizadas en la epidermis del conejillo de Indias son potenciadoras de la proteolyticidad de la pepsina",
]


def main():
    # Load environment variables
    load_dotenv()
    
    for i, statement in enumerate(statements):
        print(f"Statement {i+1}: {statement}")
        print("\n")

        # flow = FactCheckerFlow(user_input=statement)
        # result = flow.kickoff()

        # print("\nResult:")
        # print(result)
        # print("\n")

        flow2 = GetSummarizedSourceFlow(source="Christopher Columbus", target_language="Spanish")
        result = flow2.kickoff()

        print("\nResult:")
        print(result)
        print("\n")








        # fact_checker_crew.kickoff(inputs={"user_input": statement})

        # input_task_result = fact_checker_crew.tasks[0].output.json_dict
        # fact_checker_task_result = fact_checker_crew.tasks[2].output.json_dict

        # target_language = input_task_result["original_language"]
        # verification_facts = {
        #     "fragments": fact_checker_task_result["fragments"],
        #     "explanation": fact_checker_task_result["explanation"],
        #     "classification": fact_checker_task_result["classification"]
        # }

        # translation_crew.kickoff(inputs={
        #     "fact_verifier_response": verification_facts,
        #     "target_language": target_language
        # })

        # result = translation_crew.tasks[0].output.json_dict
        
        # sources = {}

        # for source in fact_checker_task_result["sources"]: 
        #     sources[source] = meta_search_tool.verify_title(meta_search_tool._normalize_text(source))   

        # result["sources"] = sources
       
        
        # with open(f"verification_results_{i}.json", "w", encoding="utf-8") as f:
        #     f.write(str(result))

        # # Create output directory if it doesn't exist
        # output_dir = "verification_results"
        # os.makedirs(output_dir, exist_ok=True)
        
        # # Create safe filename and save result
        # safe_filename = sanitize_filename(statement)
        # output_path = os.path.join(output_dir, safe_filename)
        
        # with open(output_path, "w", encoding="utf-8") as f:
        #     f.write(str(result))
        # # input("Press Enter to continue...")

        # # # Extract sources as JSON
        # # json_result = json_extraction_crew.kickoff(inputs={"fact_verifier_response": result})
        # # print("\nExtracted Sources:")
        # # print(json_result)
        # # print("\n")

        

        # # # Get Wikipedia article titles from JSON result
        # # article_titles = json_result['wikipedia_articles']
        
        # # # Search and translate for each article
        # # for article_title in article_titles:
        # #     result = meta_search_crew.kickoff(inputs={
        # #         "article_title": article_title, 
        # #         "target_language": "Spanish"
        # #     })
        # #     print(f"\nMetadata Search Results for {article_title}:")
        # #     print(result)
        # #     print("\n")

if __name__ == "__main__":
    main()
