from app.generation.llm import generate_answer


question = "What are the global logistics trends?"

context = """
Companies are focusing on green logistics.
Companies are investing in IT solutions.
E-commerce is increasing the importance of last-mile delivery.
"""


answer = generate_answer(question, context)

print(answer)